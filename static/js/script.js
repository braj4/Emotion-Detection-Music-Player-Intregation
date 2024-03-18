$(function() {
            var video = document.getElementById('video');
            var start = document.getElementById('start');
            var stop = document.getElementById('stop');
            var capture = document.getElementById('capture');
            var recom = document.getElementById('recom');
            var stream;

            start.addEventListener('click', function() {
                navigator.mediaDevices.getUserMedia({ video: true })
                    .then(function(s) {
                        stream = s;
                        video.srcObject = stream;
                        video.play();
                        recom.disabled=false;
            capture.disabled=false;
                    })
                    .catch(function(err) {
                        console.log("An error occurred: " + err);
                    });
            });

            stop.addEventListener('click', function() {
                if (stream) {
                    stream.getVideoTracks()[0].stop();
                    video.srcObject = null;
                    recom.disabled=true;
                    capture.disabled=true;
                }
            });

            capture.addEventListener('click', function() {
                var canvas = document.createElement('canvas');
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                var context = canvas.getContext('2d');
                context.drawImage(video, 0, 0, canvas.width, canvas.height);
                var dataURL = canvas.toDataURL('image/jpeg');
                var imageData = dataURL.replace(/^data:image\/(png|jpeg);base64,/, "");
                var xhr = new XMLHttpRequest();
                xhr.open('POST', '/save_image');
                xhr.setRequestHeader('Content-Type', 'application/json');
                xhr.onload = function() {
                    if (xhr.status === 200) {
                        console.log(xhr.responseText);
                    }
                };
                xhr.send(JSON.stringify({ image: imageData }));
            });

            recom.addEventListener('click', function() {
                console.log("hello");
                window.location.href = 'http://127.0.0.1:5500/templates/new_page.html';
            });
            recom.disabled=true;
            capture.disabled=true;
        });