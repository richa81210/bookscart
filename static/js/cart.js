var updateBtns = document.getElementsByClassName('update-cart')
console.log(updateBtns)
for (var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function (){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('Product ID: ', productId, 'Action: ', action)

        console.log('USER: ', user)
        if (user === 'AnonymousUser'){
            addCookieItems(productId, action)
        }
        else{
            updateUserOrder(productId, action)
        }

    })
}

function addCookieItems(productId, action){
    if (action == 'add'){
        if (cart[productId] == undefined){
            cart[productId] = {'quantity' : 1}

        }
        else{
            cart[productId]['quantity'] += 1
        }
    }

    if (action == 'remove'){
        if (cart[productId]['quantity'] == 1){
            delete cart[productId]
        }
        else{
            cart[productId]['quantity'] -= 1
        }
    }
    console.log('Cart: ', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}

function updateUserOrder(productId, action){
    console.log('User is logged in.Sending data...')

    url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'productId': productId, 'action': action, 'token': csrftoken})
    })

    .then((response) => {
        return response.json()
    })
    .then((data) =>{
        console.log('data: ', data)
        location.reload()
    })


}

