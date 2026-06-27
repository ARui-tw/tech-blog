const fs = require('fs');
const path = require('path');

function formatDuration(seconds) {
	const hours = Math.floor(seconds / 3600);
	const minutes = Math.floor((seconds % 3600) / 60);
	return hours > 0 ? `${hours}h ${minutes}m` : `${minutes} mins`;
}

function formatDate(dateString) {
	const date = new Date(dateString);
	return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

async function main() {
	const loginRes = await fetch('https://api.pocketcasts.com/user/login', {
		method: 'POST',
		headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
		body: new URLSearchParams({
			email: process.env.POCKETCASTS_EMAIL,
			password: process.env.POCKETCASTS_PASSWORD,
			scope: 'webplayer'
		})
	});
	const loginData = await loginRes.json();
	const token = loginData.token;

	const historyRes = await fetch('https://api.pocketcasts.com/user/history', {
		method: 'POST',
		headers: {
			'Authorization': `Bearer ${token}`,
			'Content-Type': 'application/json'
		}
	});
	const historyData = await historyRes.json();

	if (historyData && Array.isArray(historyData.episodes)) {
		const completed = historyData.episodes
			.filter(ep => ep.playingStatus === 3)
			.map(ep => ({
				title: ep.title,
				podcastTitle: ep.podcastTitle,
				podcastUuid: ep.podcastUuid,
				episodeUuid: ep.uuid,
				dateText: formatDate(ep.published),
				durationText: formatDuration(ep.duration)
			}));

		historyData.episodes = completed.slice(0, 30);
	}

	const outputPath = path.join(__dirname, '../data/podcast_history.json');
	fs.writeFileSync(outputPath, JSON.stringify(historyData, null, 2));
	console.log('Successfully updated the latest 30 completed podcast episodes!');
}

main().catch(console.error);
