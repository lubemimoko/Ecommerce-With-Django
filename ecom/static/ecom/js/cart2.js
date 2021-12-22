$( ".tax-edit" ).click(function() {
    $(this).toggleClass('te-open').parent;
    $('.tax-calculate').slideToggle(200);
  });
  
  $( ".if-left" ).click(function() {
    $(this).prev('.if-message').slideToggle(200);
  });
  
  $( ".bp-toggle" ).click(function() {
    $('.bonus-products').slideToggle(200);
  });

var display=""
  function getCartItems(item){
     display+= `
      <!-- begin simple product -->
            <li class="item" id="${item.id}">
              <div class="item-main cf">
                <div class="item-block ib-info cf">
                  <img class="product-img" src="${item.image}" />
                  <div class="ib-info-meta">
                    <span class="title1">${item.name}</span>
                    <span class="itemno">${item.brand}</span>
                  </div>
                </div>
                <div class="item-block ib-qty">
                  <a href="" onclick="adjustQuantity(${item.id}, 0, removeItem)">Remove Item</a> &nbsp;&nbsp; <input type="text" id="qty${item.id}" onblur="changeQuatity(${item.id}, ${item.price})" value="${item.quantity}" class="qty" />
                  <span class="price"><span>x</span> $${item.price}</span>
                </div>
                <div class="item-block ib-total-price">
                  <span class="tp-price"  id="total${item.id}">$${item.price * item.quantity}</span>
                  <span class="tp-remove"><i class="i-cancel-circle"></i></span>
                </div>         
              </div>
              <div class="item-foot cf">
                <!-- <div class="if-message"><p>Space Reserved for item/promo related messaging</p></div> -->
                <div class="if-left"><span class="if-status">In Stock</span></div>
                <div class="if-right"><!-- <span class="blue-link">Subscription Options</span> | --><span class="blue-link">Add to Wishlist</span></div>
              </div>
            </li>
      <!-- end simple product -->`;
  }


function calculateTotal() {
  let total=0

  cartStringToArray().forEach(item=>{
      total += item.price * item.quantity
  })

  return total
}


function getTotal(){
  let carttotal = calculateTotal() 
  
  let  cpt = document.getElementById("cartpagetotal")
  
  if(cpt){
    document.getElementById("cartpagetotal").innerText= "$"+carttotal
    return;
  }

  display +=` <!-- begin simple product -->
  <li class="item" style="padding-right:45% !important;"> 
    <span>Total: </span>
    <span id="cartpagetotal">$${carttotal} </span>
 
  </li>
  <!-- end simple product -->`;
}


function displayCart(){
  let cartpagedisplay = document.getElementById("cartsession")
  
  getTotal()
  
  if(cartpagedisplay){
    cartpagedisplay.innerHTML=display
  }

}
  console.log(cart)
  cart.forEach(getCartItems);   
  
  displayCart()

function removeItem(id){
  document.getElementById(id).remove()
}
  
function changeQuatity(id, price){
  
  let qty = document.getElementById("qty"+id).value
  qty = qty>=1 ? qty : 0
 
  document.getElementById("total"+id).innerText="$"+price * qty
 
  adjustQuantity(id, qty, removeItem)
  getTotal()

}



