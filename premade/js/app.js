(function() {

	/* UI Components */

	var isRunning = true;
	var button = document.getElementById('toggle');

	button.addEventListener('click', function(e){
		if(isRunning) {
			pubnub.unsubscribe({
				channel: channel
			});
			button.value = 'Stream again';
			isRunning = false;
		} else {
			getData();
			button.value = 'Stop me!';
			isRunning = true;
		}
		
	}, false);


	/* Emotional Data */

	var tally = {};

	var positiveColor = '#FF8586';
	var negativeColor = '#63A69F';
	var neutralColor = '#DECEB3';

	var positive = {
		type: 'positive',
		icon: 'grinning-face.png'
	};
	var happy = {
		type: 'positive',
		icon: 'smiling-face.png'
	};
	var lovely = {
		type: 'positive',
		icon: 'heart-eyed-happy-face.png'
	};
	var negative = {
		type: 'negative',
		icon: 'pensive-face.png'
	};
	var sad = {
		type: 'negative',
		icon: 'crying-face.png'
	};
	var angry = {
		type: 'negative',
		icon: 'angry-face.png'
	};
	var sick = {
		type: 'negative',
		icon: 'sick-face.png'
	};

	var positiveWords = [
		 'excellent', 'amazing', 'beautiful', 'nice', 'marvelous', 'magnificent', 'fabulous', 'astonishing', 'fantastic', 'peaceful', 'fortunate', 
		 'brilliant', 'glorious', 'cheerful', 'gracious', 'grateful', 'splendid', 'superb', 'honorable', 'thankful', 'inspirational',
		 'ecstatic', 'victorious', 'virtuous', 'proud', 'wonderful', 'lovely', 'delightful'
	];
	var happyWords = [
		'happy', 'lucky', 'awesome', 'excited', 'fun', 'amusing', 'amused', 'pleasant', 'pleasing', 'glad', 'enjoy',
		'jolly', 'delightful', 'joyful', 'joyous', ':-)', ':)', ':-D', ':D', '=)','☺'
	];
	var lovelyWords = [
		'love', 'adore', 'blissful', 'heartfelt', 'loving', 'lovable', 'sweetheart', 'darling', 'kawaii', 'married', 'engaged'
	];
	var negativeWords = [
		'unhappy', 'bad', 'sorry', 'annoyed', 'dislike', 'anxious', 'ashamed', 'cranky', 'crap', 'crappy', 'envy', 
		'awful', 'bored', 'boring', 'bothersome', 'bummed', 'burned', 'chaotic', 'defeated', 'devastated', 'stressed',
		'disconnected', 'discouraged', 'dishonest', 'doomed', 'dreadful', 'embarrassed', 'evicted', 'freaked out', 'frustrated', 'stupid',
		'guilty', 'hopeless', 'horrible', 'horrified', 'humiliated', 'ignorant', 'inhumane', 'cruel', 'insane', 'insecure',
		'nervous', 'offended', 'oppressed', 'overwhelmed', 'pathetic', 'powerless', 'poor', 'resentful', 'robbed', 'screwed'
	];
	var sadWords = [
		'sad', 'alone', 'anxious', 'depressed', 'disappointed', 'disappointing', 'sigh', 'sobbing', 'crying', 'cried', 
		'dumped', 'heartbroken', 'helpless', 'hurt', 'miserable', 'misunderstood', 'suicidal', ':-(', ':(', '=(', ';('
	];
	var angryWords = [
		'hate', 'damn', 'angry', 'betrayed', 'bitched','disgust', 'disturbed', 'furious', 'harassed', 'hateful', 'hostile', 'insulted',
		'irritable', 'jealous', ' rage ', 'pissed'

	];
	var sickWords = [
		'sick', ' ill ', 'under weather', 'throw up', 'threw up', 'throwing up', 'puke', 'puking', 'pain', 'hangover', 'intoxicated'
	];


	/* D3  */

	var width = 900;
	var height = 540;

	var projection = d3.geo.albersUsa();
		//.scale(900);

	var color = d3.scale.linear()
		.domain([0, 15])
		.range(['#5b5858', '#4f4d4d', '#454444', '#323131']);

	var svg = d3.select('#map').append('svg')
			.attr('width', width)
			.attr('height', height);

	var path = d3.geo.path()
	    .projection(projection);

	var g = svg.append('g');

	d3.json('json/us-states.json', function(error, topology) {
	    g.selectAll('path')
			.data(topojson.feature(topology, topology.objects.usStates).features)
			.enter()
			.append('path')
			.attr('class', function(d){ return 'states ' + d.properties.STATE_ABBR;} )
			.attr('d', path)
			.attr('fill', function(d, i) { return color(i); });
	});

	var faceIcon = svg.selectAll('image').data([0]);


	/* PubNub */

	var channel = 'pubnub-twitter';

	var pubnub = PUBNUB.init({
		subscribe_key: 'sub-c-78806dd4-42a6-11e4-aed8-02ee2ddab7fe'
	});

	// fetching previous 100 data, then realtime stream
	function getData() {
		pubnub.history({
	    	channel: channel,
	    	count: 100,
	    	callback: function(messages) {
	    		pubnub.each( messages[0], processData );
	    		getStreamData();
	    	},
	    	error: function(error) {
	    		console.log(error);
	    		if(error) {
	    			getStreamData();
	    		}
	    	}
	    });
	}

	function getStreamData() {
		pubnub.subscribe({
			channel: channel,
			callback: processData
		});
	}

	function getUserInfo(data, callback) {
		if(!data.geo) return;

		var userInfo = {};

		userInfo.lat = data.geo.coordinates[0];
		userInfo.lon = data.geo.coordinates[1];

		if(userInfo.lat === 0 && userInfo.lon === 0) return;

		var city = data.place.full_name;
		userInfo.city = city;
		userInfo.state = city.substring(city.lastIndexOf(',')+1).trim();

		userInfo.name = data.user.name;
		userInfo.screenname = data.user.screen_name;
		userInfo.avatar = data.user.profile_image_url;
		userInfo.tweet = data.text;
		userInfo.id_str = data.id_str;

		var date = new Date(parseInt(data.timestamp_ms));
		var d = date.toDateString().substr(4);
		var t = (date.getHours() > 12) ? date.getHours()-12 + ':' + date.getMinutes() + ' PM' : date.getHours() + ':' + date.getMinutes() +' AM;';

		userInfo.timestamp = t + ' - ' + d;
	
		console.log(userInfo.tweet);
		callback(userInfo);
	}

	function insertLinks(text) {            
        return text.replace(/((https?|s?ftp|ssh)\:\/\/[^"\s\<\>]*[^.,;'">\:\s\<\>\)\]\!])/g, function(url){return '<a href="'+url+'" >'+url+'</a>';});                      
    }

	function displayData(data, emotion) {

		getUserInfo(data, function(user){
			document.querySelector('.emotion').style.backgroundImage = 'url(images/'+ emotion.icon +')';

			document.querySelector('.button').href = 'https://twitter.com/' + user.screenname;
			document.querySelector('.header').style.backgroundImage = 'url('+ user.avatar +')';
			document.querySelector('.name').textContent = user.name;
			document.querySelector('.screenname').textContent = '@' + user.screenname;
			document.querySelector('.text').innerHTML = twemoji.parse(insertLinks(user.tweet));
			document.querySelector('.timestamp').textContent = user.timestamp;

			document.querySelector('.reply').href ='https://twitter.com/intent/tweet?in_reply_to=' + user.id_str;
			document.querySelector('.retweet').href = 'https://twitter.com/intent/retweet?tweet_id=' + user.id_str;
			document.querySelector('.favorite').href = 'https://twitter.com/intent/favorite?tweet_id=' + user.id_str;
			
			document.querySelector('.tweet').style.opacity = 0.9;

			if(document.querySelector('.'+user.state)) {
				tally[user.state] = (tally[user.state] || {positive: 0, negative: 0});
				tally[user.state][emotion.type] = (tally[user.state][emotion.type] || 0) + 1;

				var stateEl = document.querySelector('.'+user.state);
				stateEl.style.fill = (tally[user.state].positive > tally[user.state].negative) ? positiveColor : ((tally[user.state].positive < tally[user.state].negative) ? negativeColor :neutralColor); 

				stateEl.setAttribute('data-positive', tally[user.state].positive);
				stateEl.setAttribute('data-negative', tally[user.state].negative);
			}	

			// Place emotion icons

			var position = projection([user.lon, user.lat]);
			if(position === null) return;

			faceIcon.enter()
				.append('svg:image')
				.attr('xlink:href', 'images/'+ emotion.icon)
				.attr('width', '26').attr('height', '26')
           		.attr('transform', function(d) {return 'translate(' + position + ')';});
		});
	}

	function processData(data) {
		if(!data || !data.place || !data.lang) return; 
		if(data.place.country_code !== 'US') return;
		//if(data.lang !== 'en') return;

		if (positiveWords.some(function(v) { return data.text.toLowerCase().indexOf(v) !== -1; })) {
			displayData(data, positive);
		} else if (happyWords.some(function(v) { return data.text.toLowerCase().indexOf(v) !== -1; })) {
			displayData(data, happy);
		} else if (lovelyWords.some(function(v) { return data.text.toLowerCase().indexOf(v) !== -1; })) {
			displayData(data, lovely);
		} else if (negativeWords.some(function(v) { return data.text.toLowerCase().indexOf(v) !== -1; })) {
			displayData(data, negative);
		} else if (sadWords.some(function(v) { return data.text.toLowerCase().indexOf(v) !== -1; })) {
			displayData(data, sad);
		} else if (angryWords.some(function(v) { return data.text.toLowerCase().indexOf(v) !== -1; })) {
			displayData(data, angry);
		} else if (sickWords.some(function(v) { return data.text.toLowerCase().indexOf(v) !== -1; })) {
			displayData(data, sick);
		}
	}

	getData();
	
})();