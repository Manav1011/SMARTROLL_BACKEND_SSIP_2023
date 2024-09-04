self.addEventListener('push', (event) => {
  const options = { body: event.data.text(), icon: '/static/images/smartroll_logo.png' }
  event.waitUntil(self.registration.showNotification('Hello Professor!!', options))
})
