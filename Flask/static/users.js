Vue.component("userdisplay", {
  props: ['users'],
  template:
  `
  <div>
  <li
  v-for="user in users"
  v-bind:key="user.id"
  v-bind:group="user">Usuario 1
    <i>
      <i class="fa fa-close pull-right" style="color:red"></i>
    </i>
  </li>
  </div>
  `
});
Vue.component("userInfoBox", {
  props:["user"],
  template:
  `
  
  `
});

