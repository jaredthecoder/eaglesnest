<!DOCTYPE html>
<html lang="en" ng-app="BirdsEye">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="description" content="BirdsEye, a Twitter Sentiment Visualizer. View Twitter like you never have before. From above.">
    <meta name="author" content="Jared Smith">

    <title>BirdsEye</title>

    <link href="http://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css" rel="stylesheet">
    <link rel="stylesheet" href="static/css/vendor/leaflet.css">
    <!--[if lte IE 8]><link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.7.2/leaflet.ie.css" /><![endif]-->
    <link rel="stylesheet" href="static/css/vendor/leaflet-control-credits.css">


    <link rel="stylesheet" href="static/css/vendor/leaflet-sidebar.css" />
    <!-- Fix for older browsers (IE) -->
    <!--[if lt IE 9]>
        <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->

    <style>
        @import url(http://fonts.googleapis.com/css?family=Raleway:400,500,600,700,300,200);

        * {
            font-family: 'Raleway', Sans-Serif;
        }

        body {
            padding: 0;
            margin: 0;
        }

        html, body, #map {
            height: 100%;
        }

        .lorem {
            font-style: italic;
            color: #AAA;
        }
        .tweet-item {
            height: 25px;
            background-color: #0E0E0E;
            border-left: 5px solid #333;
        }

        .tweet-item img {
            height: 25px;
            width: 25px;
            opacity: 0.75;
        }
            
        .tweet-item .text {
            position: relative;
            top: -8px;
            font-size: 12px;
        }

        .negative {
            border-color: red;
        }

        .positive {
            border-color: green;
        }

        /* D3.js Ping element styles */

        circle.ping {
             stroke: #222;
             fill: yellow;
        }

        circle.green {
            stroke: #000;
            stroke-width: 1px;
            fill: green;
        }

        circle.red {
            stroke: #000;
            stroke-width: 1px;
            fill: red;
        }

        circle.gray {
            stroke: #000;
            stroke-width: 1px;
            fill: grey;
        }

    </style>
</head>
<body>
    <div id="sidebar" class="sidebar collapsed">
        <!-- Nav tabs -->
        <ul class="sidebar-tabs" role="tablist">
            <li><a href="#users" role="tab"><i class="fa fa-users"></i></a></li>
            <li><a href="#analytics" role="tab"><i class="fa fa-area-chart"></i></a></li>
            <li><a href="#about" role="tab"><i class="fa fa-cog"></i></a></li>
            <li><a href="https://github.com/jaredmichaelsmith/birdseye"><i class="fa fa-github"></i></a></li>
            <li><a href="https://twitter.com/share"><i class="fa fa-twitter"></i></a></li>
        </ul>

        <!-- Tab panes -->
        <div class="sidebar-content active">
            <div class="sidebar-pane" id="users">
                <div id="tweet-hud" ng-controller="TweetHud">
                    <h1>Users</h1>
                    <!-- Repeats for every Tweet in the $scope.tweets model -->
                    {% raw %}
                    <div ng-repeat="tweet in tweets" class="tweet-item {{tweet.sentiment}}">
                        <img ng-src="{{tweet.user_profile_image_url}}" />
                        <span class="text"><a href="{{tweet.user_profile_image_url}}" target="_blank">{{ tweet.user_screen_name}}</a></span>
                    </div>
                    {% endraw %}
                </div>
            </div>
            <div class="sidebar-pane" id="analytics"><h1>Analytics</h1></div>
            <div class="sidebar-pane" id="about"><h1>About</h1></div>
        </div>
    </div>

    <div id="map" class="sidebar-map"></div>

    <!--
    <a href="https://github.com/jaredmichaelsmith/birdseye"><img style="position: fixed; top: 0; right: 0; border: 0;" src="https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png" alt="Fork me on GitHub"></a>
    -->

    <script src="static/js/vendor/sockjs-0.3.js"></script>
    <script src="static/js/vendor/stomp.min.js"></script>
    <script src="static/js/vendor/d3.min.js"></script>
    <script src="static/js/vendor/leaflet.js"></script>
    <script src="static/js/vendor/leaflet-d3.min.js"></script>
    <script src="static/js/vendor/leaflet-sidebar.min.js"></script>
    <script src="static/js/vendor/leaflet-control-credits.js"></script>
    <script src="static/js/vendor/angular.js"></script>
    <script src="static/js/vendor/angular-resource.js"></script>

    <script>
        var app = angular.module('BirdsEye', ['ngResource']);
        
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
    </script>
</body>
</html>
