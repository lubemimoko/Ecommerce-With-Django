//compare
let compare = document.getElementsByClassName("add-cart");
let maincontainer = document.getElementsByClassName("compare")[0]
for(let i = 0;i < compare.length; i++){
    compare[i].addEventListener("click", compared)
}

function compared(event) {

    let com = event.target
    let comparent = com.parentElement
    let comgrand = comparent.parentElement
    let price = comgrand.children[4].innerText.replace("$", "")
    let image = comgrand.children[0].src
    let brand = comgrand.children[2].innerText
    let name = comgrand.children[3].innerText
    let id=comgrand.children[3].getAttribute("id")
    
    addToCart(id, price, image, name, brand)
    
    let item_Container = document.createElement("aside")
    item_Container.innerHTML =
    `<img src="${image}" alt=""/>
    <p>${brand}</p>
    <p>${name}</p>
    <p>${price}</p>
`
    maincontainer.append(item_Container)
}

let cart = [];                       


( 
    ()=>{
        // localStorage.setItem("cart", '[{"id": 1}, {"id":2}]');
          numberInCart()
            ItemsInCart()
        }
)()

//send to django
function djangocart(product, quantity, url="/cart/"){
    
    //terminate function when user is not logged in
    if(!userid || userid < 0 || !quantity ){return}

    let formData = JSON.stringify({"product":product, "quantity":quantity}); //Array 
    let csrftoken = $("input[name='csrfmiddlewaretoken']")[0].defaultValue
    let headers={
      'Content-Type':'application/json',
      'X-CSRFToken':csrftoken,
    }
   
    $.ajax({
        url : url, // Url of backend (can be python, php, etc..)
        type: "POST", // data type (can be get, post, put, delete)
        dataType:'json',
        data : formData, // data in json format
        headers:headers, 
        success: function(res) {
          console.log(res);
        },
        error: function (res) {
        console.log(res);
        }
    });
  }
  


  // get items from cart            
function getCart(){ 
    return localStorage.getItem("cart") ?? "[]"    
}            
            
function setCart(arr){            
    return localStorage.setItem("cart", JSON.stringify(arr) );
}            
//when page loads, it should calculate the number of items in cart
function numberInCart() {
    cartArray = cartStringToArray( getCart() )
    cartcount = cartArray.length
    document.querySelector("#btn-compare").innerHTML = cartcount;
    
}

//From Cart String to Array of Objects            
function cartStringToArray(object='empty'){
    if (object == 'empty'){object = getCart();}
    // console.log(object)
    cart = JSON.parse(object)
    return cart
}  

//func
function ItemsInCart(){
    
    let arr = cartStringToArray()
    arr.forEach(alreadyInCart); 
}            
            
                        
//when page loads already in cart
function alreadyInCart(id){
    // console.log(id)
    
    if (typeof(id) == 'number' && document.getElementById("write"+id)){
        document.getElementById("write"+id).innerText="Already In Cart"
    }else if(document.getElementById("write"+id.id)){
        document.getElementById("write"+id.id).innerText="Already In Cart"
    }
}                       

//when items are added to cart do the first 2
function addToCart(id, price, image, name, brand, quantity=1){                       
    //check if id exist in cart                       
    stringcart = getCart()                          
        // console.log(stringcart)                         
    if(stringcart.indexOf('"id":"'+id) > 0){                       
        alert("Item is Already In Cart"); return;                   
    }                   
    //form object                       
    newitem = {"id":id, "price":price, "image":image, "name":name, "brand":brand, "quantity":quantity}                      
    //push to cart                       
    cartStringToArray().push(newitem)                                

    //send cart to django if logged in
    djangocart(id, quantity, url="/cart/")

    // update localstorage
    setCart(cart)             
                                    
    //number in cart and already in cart                       
    numberInCart()
    ItemsInCart()                      
}

function writeup(id){
    document.getElementById("write"+id).innerText="Add To Cart"
}    

//when items are removed from cart do the first 2 also
function remove(id, func){                       
    //grab glocal scope cart and splice item from array                                  
    cartStringToArray().forEach((ele, ind) =>{
        if(ele.id == id){
            cartStringToArray().splice(ind, 1);
            console.log("remove", cart, ind, id, ele.id)
            func(id)
        }
    })                                                

    console.log("after remove cart", cart)
    //delete cart in django if logged in
    djangocart(id, -1, "/deleteitem/")
    // djangocart(product, quantity, url="/cart/")

    setCart(cart)                      
                                   
    //number in cart and already in cart                      
    numberInCart()
    ItemsInCart()              
}                      
   
//when adjust quantity                      
function adjustQuantity(id, quantity, func=writeup){ 
    if(quantity < 1){

        // below 1 just only adjust quantity 
        console.log("adjustQuantity")
       return remove(id, func)
    }else if(quantity >= 1){
        // above 0 call remove and pass id
        cartStringToArray().forEach(ele =>{ 
            if(ele.id == id){
                ele.quantity = quantity
            }  
        })                          
        
        //send cart to django if logged in
        djangocart(id, quantity, url="/cart/")

        setCart(cart) 
    }
                                            
}    
                        
  