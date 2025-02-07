import axios from 'axios'
import { useRouter } from 'vue-router'
import { useNotification } from '@kyvg/vue3-notification'


// redirect and notify
export class redirectNotify {
  constructor() {
    this.router = useRouter()
    this.notification = useNotification()
    this.path = '/'
    this.title = 'Sign Up Not Allowed'
    this.text = 'You already logged in!'
  }

  update(path, msg) {
    if (path) {
      this.path = path
    }

    if (msg) {
      this.title = msg.title
      this.text = msg.text
    }

    this.use()
  }

  use() {
    this.notification.notify({ title: this.title, text: this.text, })
    this.router.push(this.path)
  }
}