Vue.component("userdisplay", {
  props: ['users'],
  template:
  `
  <div>
  <userInfoBox
    v-for="user in users"
    v-bind:key="user.id"
    v-bind:group="user"
  ></userInfoBox>
  </div>
  `
});
Vue.component("userInfoBox", {
  props:["user"],
  template:
  `
  <li>Usuario 1
    <i>
      <i class="fa fa-close pull-right" style="color:red"></i>
    </i>
  </li>
  `
});

