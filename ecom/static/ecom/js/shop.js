$(window).on('load',function(){
    $('.carousel').owlCarousel({
        margin: 10,
        loop: true,
        autoplay: true,
        autoplayTimeout: 2000,
        autoplayHoverPause: true,
            responsive:{
                0:{
                    items: 1,
                    nav: false
                },
        
                600:{
                    items: 2,
                    nav: false
                },
        
                1000:{
                    items: 3,
                    nav: false
                }
            }
        })
    })
    



window.onload = ()=>{
    const grabber = document.querySelector(".menu-bar");
    let grab = document.querySelector(".item-gallery")
    let grab1 = document.getElementById("shoe")
    let grab2 = document.getElementById("watch")
    window.addEventListener('scroll',double);
    window.addEventListener('scroll',double2);
    function double() {
        if(window.scrollY >= 500){
            grab.classList.add("scale")
            grabber.classList.add("animate")
        }
    }
    function double2() {
        if(window.scrollY >= 100){
            grab.classList.add("scale")
            grab1.classList.add("scale")
            grab2.classList.add("scale")
        }
    }
}

window.addEventListener('load',(event)=>{
    let loaded = document.querySelector(".topsellers");
    let loaded1 = document.getElementsByTagName("header")[0]
    loaded.classList.add("animater")
    loaded1.classList.add("animater")
})


var loader = document.getElementById("loader");//preloader jquery script

window.addEventListener("load",vanish)

function vanish() {
    loader.classList.add("vanish")
}

$(".hamburger").click(function(){
    $(".navbar").toggleClass("move")
})

$(window).on("scroll", function () {
    if ($(window).scrollTop()){
        $("nav").addClass("black")
        $("h4").addClass("black")
    }
    else{
        $("nav").removeClass("black")
        $("h4").removeClass("black")
    }
})


let filterContainer = document.querySelector(".brands"),//button active style switch script and filter script
galleryItems = document.querySelectorAll(".bags-unit");

filterContainer.addEventListener("click",(event) =>{
    if(event.target.classList.contains("btn")){
        //deactivate existing active 'filter-item'
        filterContainer.querySelector(".active").classList.remove("active");
        //activate new 'filter-item'
        event.target.classList.add("active");
        const filterValue = event.target.getAttribute("data-filter");//filter script
        console.log(filterValue)        
        galleryItems.forEach((item)=>{
            if(item.classList.contains(filterValue) || filterValue === "all"){
                item.classList.add("show")
                item.classList.remove("hide")
            }else{
                item.classList.remove("show")
                item.classList.add("hide")
            }
        })
    }
});


let shoefilterContainer = document.querySelector(".shoe-brands"),//filter and button chasnge for shoe category
shoegalleryItem = document.querySelectorAll(".shoes-unit");

if(shoefilterContainer){

    shoefilterContainer.addEventListener("click",(event) =>{
        if(event.target.classList.contains("btn-shoes")){
            //deactivate existing active 'filter-item'
            shoefilterContainer.querySelector(".active").classList.remove("active");
            //activate new 'filter-item'
            event.target.classList.add("active");
            const shoefilterValue = event.target.getAttribute("data-filter");
            shoegalleryItem.forEach((item)=>{
                if(item.classList.contains(shoefilterValue) || shoefilterValue === "all"){
                    item.classList.add("show")
                    item.classList.remove("hide")
                }else{
                    item.classList.remove("show")
                    item.classList.add("hide")
                }
            })
        }
    });
}
let watchfilterContainer = document.querySelector(".watch-brands"),////filter and button chasnge for shoe category
watchgalleryItem = document.querySelectorAll(".watch-unit");

if(watchfilterContainer){

    watchfilterContainer.addEventListener("click",(event) =>{
        if(event.target.classList.contains("btn-watch")){
            //deactivate existing active 'filter-item'
            watchfilterContainer.querySelector(".active").classList.remove("active");
            //activate new 'filter-item'
            event.target.classList.add("active");
            const watchfilterValue = event.target.getAttribute("data-filter");
            watchgalleryItem.forEach((item)=>{
                if(item.classList.contains(watchfilterValue) || watchfilterValue === "all"){
                    item.classList.add("show")
                    item.classList.remove("hide")
                }else{
                    item.classList.remove("show")
                    item.classList.add("hide")
                }
            })
        }
    });
}
