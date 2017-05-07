<template>
  <section class="login-info">
    <div class="container">
      <div class="row main">
        <div class="form-header">
          <h1 class="text-center ">Login</h1>
        </div>
        <div class="main-content">

          <div class="input-group ">
            <span class="input-group-addon"><span class="glyphicon glyphicon-envelope" aria-hidden="true"></span></span>
            <input id="email" type="text" v-model="email" class="form-control" name="email" placeholder="Enter your Email">
          </div>
          <div class="input-group">
            <span class="input-group-addon"><span class="glyphicon glyphicon-lock" aria-hidden="true"></span></span>
            <input id="password" type="password" v-model="password" class="form-control" name="password" placeholder="Enter your Password">
          </div>

          <div class="form-group ">
            <a href="#" type="button" class="btn btn-danger btn-lg btn-block login-button" @click="login">login</a>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
  import loginMixins from './mixins/login_mixins'
  export default {
    mixins: [loginMixins]
  }
</script>
