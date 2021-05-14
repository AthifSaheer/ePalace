// Image each one selection and it will disaplayed ==================
mainImgBig = document.getElementById('imgbig')
img1big = document.getElementById('img1-big')
img2big = document.getElementById('img2-big')
img3big = document.getElementById('img3-big')

function imfunc(){
    mainImgBig.style.display = 'block'
    img1big.style.display = 'none'
    img2big.style.display = 'none'
    img3big.style.display = 'none'
}
function img1Func(){
    mainImgBig.style.display = 'none'
    img1big.style.display = 'block'
    img2big.style.display = 'none'
    img3big.style.display = 'none'
}
function img2Func(){
    mainImgBig.style.display = 'none'
    img1big.style.display = 'none'
    img2big.style.display = 'block'
    img3big.style.display = 'none'
}
function img3Func(){
    mainImgBig.style.display = 'none'
    img1big.style.display = 'none'
    img2big.style.display = 'none'
    img3big.style.display = 'block'
}


//====================== Image Zoom Script====================================


function imageZoom(imgID, resultID) {
  var img, lens, result, cx, cy;
  img = document.getElementsByClassName('imgID')[0]
  result = document.getElementsByClassName('resultID')[0]
  /*create lens:*/
  lens = document.createElement("DIV");
  lens.setAttribute("class", "img-zoom-lens");
  /*insert lens:*/
  img.parentElement.insertBefore(lens, img);
  /*calculate the ratio between result DIV and lens:*/
  cx = result.offsetWidth / lens.offsetWidth;
  cy = result.offsetHeight / lens.offsetHeight;
  /*set background properties for the result DIV:*/
  result.style.backgroundImage = "url('" + img.src + "')";
  result.style.backgroundSize = (img.width * cx) + "px " + (img.height * cy) + "px";
  /*execute a function when someone moves the cursor over the image, or the lens:*/
  lens.addEventListener("mousemove", moveLens);
  img.addEventListener("mousemove", moveLens);
  /*and also for touch screens:*/
  lens.addEventListener("touchmove", moveLens);
  img.addEventListener("touchmove", moveLens);
  function moveLens(e) {
    var pos, x, y;
    /*prevent any other actions that may occur when moving over the image:*/
    e.preventDefault();
    /*get the cursor's x and y positions:*/
    pos = getCursorPos(e);
    /*calculate the position of the lens:*/
    x = pos.x - (lens.offsetWidth / 2);
    y = pos.y - (lens.offsetHeight / 2);
    /*prevent the lens from being positioned outside the image:*/
    if (x > img.width - lens.offsetWidth) {x = img.width - lens.offsetWidth;}
    if (x < 0) {x = 0;}
    if (y > img.height - lens.offsetHeight) {y = img.height - lens.offsetHeight;}
    if (y < 0) {y = 0;}
    /*set the position of the lens:*/
    lens.style.left = x + "px";
    lens.style.top = y + "px";
    /*display what the lens "sees":*/
    result.style.backgroundPosition = "-" + (x * cx) + "px -" + (y * cy) + "px";
  }
  function getCursorPos(e) {
    var a, x = 0, y = 0;
    e = e || window.event;
    /*get the x and y positions of the image:*/
    a = img.getBoundingClientRect();
    /*calculate the cursor's x and y coordinates, relative to the image:*/
    x = e.pageX - a.left;
    y = e.pageY - a.top;
    /*consider any page scrolling:*/
    x = x - window.pageXOffset;
    y = y - window.pageYOffset;
    return {x : x, y : y};
  }
}


// Initiate zoom effect:
imageZoom("myimage", "myresult");