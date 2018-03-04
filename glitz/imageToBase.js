// https://gist.github.com/HereChen/e173c64090bea2e2fa51

/**
 * version1: convert online image
 * @param  {String}   url
 * @param  {Function} callback
 * @param  {String}   [outputFormat='image/png']
 * @author HaNdTriX
 * @example
    convertImgToBase64('http://goo.gl/AOxHAL', function(base64Img){
        console.log('IMAGE:',base64Img);
    })
 */
function convertImgToBase64(url, callback, outputFormat){
    var img = new Image();
    img.crossOrigin = 'Anonymous';
    img.onload = function(){
        var canvas = document.createElement('CANVAS');
        var ctx = canvas.getContext('2d');
        canvas.height = this.height;
        canvas.width = this.width;
        ctx.drawImage(this,0,0);
        var dataURL = canvas.toDataURL(outputFormat || 'image/png');
        callback(dataURL);
        canvas = null; 
    };
    img.src = url;
}

// https://davidwalsh.name/convert-image-data-uri-javascript
function getDataUri(url) {
    var image = new Image();

    image.onload = function () {
        var canvas = document.createElement('canvas');
        canvas.width = this.naturalWidth; // or 'width' if you want a special/scaled size
        canvas.height = this.naturalHeight; // or 'height' if you want a special/scaled size

        canvas.getContext('2d').drawImage(this, 0, 0);

        // Get raw image data
        // var data = canvas.toDataURL('image/png').replace(/^data:image\/(png|jpg);base64,/, '');
        var data = canvas.toDataURL("image/jpeg").replace(/^data:image\/(png|jpg);base64,/, '');
        console.log(data);
        // // ... or get as Data URI
        // callback(canvas.toDataURL('image/png'));
        canvas.toBlob(function (blob) {
            var reader = new FileReader();

            reader.onloadend = function () {
                // console.log(reader.result);
                // processImage(reader.result);
                // analyze_data(reader.result);

            }

            reader.readAsBinaryString(blob);
        });
    };
    image.crossOrigin = "Anonymous";
    image.src = url;
}

function analyze_data(blob)
{
    var myReader = new FileReader();
    myReader.readAsArrayBuffer(blob)
    
    myReader.addEventListener("loadend", function(e)
    {
        var buffer = e.srcElement.result;//arraybuffer object
        processImage(buffer);
    });
}


function getImageBlobAndProcess(url) {
    var oReq = new XMLHttpRequest();

    oReq.open("GET", url, true);
    oReq.responseType = "arraybuffer";

    oReq.onload = function(oEvent) {
        // var blob = oReq.response;
        var blob = new Blob([oReq.response], {type: "image/jpg"})
        processImage(blob);
        // analyze_data(blob);
    };
    oReq.send();
}

function getImageBase64(url) {
    var myCanvas = $('<canvas/>');
    var myImageSrc = myCanvas.attr('src', url);
    myCanvas.attr('src', myImageSrc);
    var dataInBase64 = $(myCanvas)[0].toDataURL('image/jpg').replace(/data\:image\/png;base64,/, '');

    return dataInBase64;
}

function binEncode(data) {
    var binArray = []
    var datEncode = "";

    for (i=0; i < data.length; i++) {
        binArray.push(data[i].charCodeAt(0).toString(2)); 
    } 
    for (j=0; j < binArray.length; j++) {
        var pad = padding_left(binArray[j], '0', 8);
        datEncode += pad + ' '; 
    }
    function padding_left(s, c, n) { if (! s || ! c || s.length >= n) {
        return s;
    }
    var max = (n - s.length)/c.length;
    for (var i = 0; i < max; i++) {
        s = c + s; } return s;
    }
    return binArray;
}

// convertImgToBase64("http://localhost:5000/{{ glitz_details[0] }}", function(base64Img){
//     // console.log(base64Img.replace(/data\:image\/png;base64,/, ''));
//     googleVisionProcessImage(base64Img.replace(/data\:image\/png;base64,/, ''));            
// });

// var data = getImageBase64("http://localhost:5000/{{ glitz_details[0] }}");
// getDataUri("http://localhost:5000/{{ glitz_details[0] }}");
// getDataUri("https://gloimg.drlcdn.com/L/pdm-product-pic/Clothing/2018/02/03/goods-img/1517858715287316700.jpg");
// var imageBase64 = getImageBase64("http://localhost:5000/glitz/221098.max-620x600.jpg");
// var binary = binEncode(imageBase64);
// console.log(binary);
