import $ from 'jquery'
var loginMixins = {
  data: function () {
    return {
      email: '',
      password: ''
    }
  },
  methods: {
    login: function (event) {
      event.preventDefault()
      var data = 'email=' + this.email + '&password=' + this.password
      $.ajax({
        // url: this.getBaseUrl() + 'account/login', When Server Present
        url: 'http://localhost:8000/profiles/login/',
        type: 'POST',
        data: data,
        success: function (data) {
          console.log(data)
        }
      })
    }
  }

}
export default loginMixins
