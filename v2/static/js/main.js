var app = angular.module('BirdsEye', ['ngResource', 'ngRoute']);

app.controller('TweetHud', function($scope, $resource, $timeout, $rootScope) {

    var TWEET_SAMPLE_SIZE = 50;
    $scope.init = function () {
        $scope.tweets = [];

        // Define the center of the map.
        var center = [39.82, -98.58];

        var scaleControl = L.control.scale({
            position: 'bottomright'
        });

        // Get the basemap 'Dark Matter' from CartoDB and create the basemap layer.
        var basemapLayer = L.tileLayer('http://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png',{
                attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="http://cartodb.com/attributions">CartoDB</a>'
        });

        // Create the map object.
        var map = L.map('map', {
            layers: [basemapLayer],
            scrollWheelZoom: true,
            minZoom: 3,
            maxZoom: 8,
            touchZoom: true,
            doubleClickZoom: true,
            dragging: true,
            center: new L.LatLng(center[0], center[1]),
            zoom:5
        });

        L.controlCredits({
            image: "static/img/birdseye.png",
            link: "https://jaredmichaelsmith.com",
            text: "View Twitter like never before. From Above."
        }).addTo(map);

        // Configure a ping layer.
        var options = {
            lng: function(d){ return d[0]; },
            lat: function(d){ return d[1]; },
            duration: 800,
            efficient: {
                enabled: true,
                fps: 8
            }
        };

        var sidebar = L.control.sidebar('sidebar').addTo(map);

        // Create the ping layer and add it to the map.
        var pingLayer = L.pingLayer(options).addTo(map);

        // Change the radius and the opacity of the ping marker.
        pingLayer.radiusScale().range([2, 18]);
        pingLayer.opacityScale().range([1, 0]);

        // Establish a web socket connection through the STOMP protocol so that we can get data
        // from the Flask server.
        var ws = new SockJS('http://' + window.location.hostname + ':15674/stomp');
        var client = Stomp.over(ws);

        // Disable heartbeat functionality as it is not supported by this STOMP setup.
        client.heartbeat.incoming = 0;
        client.heartbeat.outgoing = 0;

        // Called on error.
        var on_error = function(error) {
            console.log('error');
        };

        // Called when a message is recieved from the queue.
        var recv_message = function(message) {
            var tweet = JSON.parse(message.body);
            pingLayer.ping([tweet.lon, tweet.lat], tweet.color);
            addTweet(tweet);
        };

        // Called when a connection is made to the web socket.
        var on_connect = function() {
            var subscription = client.subscribe("/amq/queue/twitter_sentiment_feed", recv_message); 
        };

        // Establish a connection with the broker.
        client.connect('guest', 'guest',  on_connect, on_error, '/');
    };

    function addTweet (tweet) {

        if (tweet.color === 'red') {
            tweet.sentiment = 'negative';
        } else if (tweet.color === 'green') {
            tweet.sentiment = 'positive';
        } else if (tweet.color === 'gray') {
            tweet.sentiment = 'neutral';
        }

        $scope.$apply(function () {
            $scope.tweets.unshift(tweet);
        });

          if ($scope.tweets.length > TWEET_SAMPLE_SIZE) {
            $scope.$apply(function () {
                $scope.tweets.pop();
            });
        }
    }

    $scope.init();
});
