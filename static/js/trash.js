function remove_from_trash(pid) {

	let td = document.getElementById('tr-' + pid)

	let xhr = new XMLHttpRequest()
	xhr.open('POST', '/remove_product_from_trash', true)
	xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded")
	xhr.responseType = "json"

	xhr.onload = () => {
		if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {

			let price = parseFloat(document.getElementById('total_price').innerText.replace('Общая стоимость заказа: ', '').replace(' ₽', ''))
			price -= xhr.response['amount']
			document.getElementById('total_price').innerText = `Общая стоимость заказа: ${price} ₽`
			td.remove()

		}
	};

    xhr.send(`pid=${pid}`);

}


function update_count(pid) {

	let count = document.getElementById(`p-${pid}`).value
	if (!count) count = 0

	let xhr = new XMLHttpRequest()
	xhr.open('POST', '/update_pot_count', true)
	xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded")
	xhr.responseType = "json"

	xhr.onload = () => {
		if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {

			let price = parseFloat(document.getElementById('total_price').innerText.replace('Общая стоимость заказа: ', '').replace(' ₽', ''))
			price = price - (parseFloat(xhr.response['price']) * parseFloat(xhr.response['old'])) + (parseFloat(xhr.response['price']) * parseFloat(xhr.response['new']))
			document.getElementById('total_price').innerText = `Общая стоимость заказа: ${price} ₽`

		}
	};

    xhr.send(`pid=${pid}&count=${count}`);
}


function send_order() {
	let xhr = new XMLHttpRequest()
	xhr.open('POST', '/send_order', true)
	xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded")
	xhr.responseType = "json"

	xhr.onload = () => {
		if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {

			alert('Заказ отправлен!')
			window.location.href = '/pricelists'

		}
	};

    xhr.send(``);
}
