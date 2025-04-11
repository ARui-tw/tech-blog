import torch
import torch.nn.functional as F
from transformers.modeling_outputs import CausalLMOutputWithCrossAttentions, BaseModelOutputWithPooling
from transformers import GenerationMixin, AutoConfig
from transformers.modeling_utils import PreTrainedModel
from transformers import BlipForQuestionAnswering 
import os
import random
from time import sleep

class PaddedDecoder(torch.nn.Module):
    def __init__(self, model):
        super().__init__()
        self.decoder = model

    def forward(
            self,
            input_ids, 
            encoder_hidden_states=None, 
            encoder_attention_mask=None,
            attention_mask=None,
            current_length=None,
            **kwargs
        ):

        output = self.decoder(
            input_ids=input_ids,
            encoder_hidden_states=encoder_hidden_states,
            encoder_attention_mask=encoder_attention_mask,
            attention_mask=attention_mask,
            use_cache=False,
        )
        result = torch.take_along_dim(output['logits'], current_length.view(1, -1, 1), dim=1)

        return result

class DecoderOutputFormatter(torch.nn.Module):
    def __init__(self, decoder):
        super().__init__()
        self.decoder = decoder

    def forward(
            self, 
            input_ids,
            encoder_hidden_states=None,
            encoder_attention_mask=None,
            attention_mask=None,
            current_length=None,
            **kwargs
        ):
        logits = self.decoder(
            input_ids,
            encoder_hidden_states,
            encoder_attention_mask,
            attention_mask,
            current_length,
            **kwargs
        )

        return CausalLMOutputWithCrossAttentions(
            logits=logits,
        )

class DecoderPaddedGenerator(PreTrainedModel, GenerationMixin):

    @classmethod
    def from_model(cls, model):
        generator = cls(model.config)
        generator.decoder = DecoderOutputFormatter(PaddedDecoder(model))

        return generator

    @classmethod
    def from_pretrained(cls, directory):
        config = AutoConfig.from_pretrained(directory)
        obj = cls(config)
        obj.decoder = DecoderOutputFormatter(torch.jit.load(os.path.join(directory, "text_decoder.pt")))


        return obj
    
    @property
    def device(self):  # Attribute required by beam search
        return torch.device('cpu')

    def prepare_inputs_for_generation(
        self,
        input_ids,
        encoder_hidden_states=None,
        encoder_attention_mask=None,
        **kwargs,
    ):
        current_length = input_ids.shape[-1]
        pad_token_id = self.config.pad_token_id
        pad_size = self.config.max_length - current_length
        input_ids = F.pad(input_ids, (0, pad_size), value=pad_token_id)

        attention_mask = torch.ones_like(input_ids)
        attention_mask[:, current_length:] = 0

        return dict(
            input_ids=input_ids,
            encoder_hidden_states=encoder_hidden_states,
            encoder_attention_mask=encoder_attention_mask,
            attention_mask=attention_mask,
            current_length=torch.tensor([current_length - 1]),
        )
            

    def forward(
            self,
            input_ids, 
            encoder_hidden_states=None, 
            encoder_attention_mask=None,
            attention_mask=None,
            current_length=None,
            **kwargs
        ):

        return self.decoder(
            input_ids,
            encoder_hidden_states,
            encoder_attention_mask,
            attention_mask,
            current_length,
        )

class NeuronVisonModel(torch.nn.Module):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def forward(self, pixel_values):
        return self.model(pixel_values=pixel_values, interpolate_pos_encoding=False)

class VisionModelWrapper(torch.nn.Module):
    def __init__(self, model):
        super().__init__()
        self.model = NeuronVisonModel(model)

    @classmethod
    def from_model(cls, model):
        wrapper = cls(model)
        wrapper.model = model

        return wrapper

    def forward(self, pixel_values, interpolate_pos_encoding):
        output = self.model(pixel_values)

        return BaseModelOutputWithPooling(
            last_hidden_state=output['last_hidden_state'],
            pooler_output=output['pooler_output'],
        )

class NeuronTextEncoder(torch.nn.Module):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def forward(self, input_ids, attention_mask, encoder_hidden_states, encoder_attention_mask):
        output = self.model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            encoder_hidden_states=encoder_hidden_states,
            encoder_attention_mask=encoder_attention_mask,
            return_dict=False,
        )

        return output[0]

class TextEncoderWrapper(torch.nn.Module):
    def __init__(self, model):
        super().__init__()
        self.model = NeuronTextEncoder(model)

    @classmethod
    def from_model(cls, model):
        wrapper = cls(model)
        wrapper.model = model

        return wrapper

    def forward(self, input_ids, attention_mask, encoder_hidden_states, encoder_attention_mask, return_dict):
        output = self.model(input_ids, attention_mask, encoder_hidden_states, encoder_attention_mask)
        return (output, )

class NeuronBlipForQuestionAnswering(BlipForQuestionAnswering):
    def __init__(self, config):
        super().__init__(config)
    
    @classmethod
    def from_pretrained(cls, directory, num_models):
        config = AutoConfig.from_pretrained(directory)

        models = []
        for i in range(num_models):
            models.append(cls(config))
        
        for i in range(num_models):
            models[i].vision_model = VisionModelWrapper.from_model(torch.jit.load(os.path.join(directory, 'vision_model.pt')))
        
        for i in range(num_models):
            models[i].text_decoder = DecoderPaddedGenerator.from_pretrained(directory)
        
        for i in range(num_models):
            models[i].text_encoder = TextEncoderWrapper.from_model(torch.jit.load(os.path.join(directory, 'text_encoder.pt')))

        return models