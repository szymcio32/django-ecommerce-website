// get cookie value
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function updateTotalCartItems(total_items){
    document.querySelector('#cart-total-items').innerHTML = total_items;
}

function showAlert(msg, cls, parent, before_elem){
    const div = document.createElement('div');
    div.className = `alert ${cls}`;
    div.appendChild(document.createTextNode(msg));
    const container_div = document.querySelector(parent);
    const card_div = document.querySelector(before_elem);
    container_div.insertBefore(div, card_div);

    setTimeout( () => div.remove(), 2000);
}