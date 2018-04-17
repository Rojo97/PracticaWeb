Vue.component("groupdisplay", {
  props: ['groups'],
  template:
  `
  <div>
  <groupInfoBox
    v-for="group in groups"
    v-bind:key="group.id"
    v-bind:group="group"
  ></groupInfoBox>
  </div>
  `
});
Vue.component("groupInfoBox", {
  props:["group"],
  template:
  `
  <div style="margin-bottom:2%; margin-left:10%; margin-right:15%">  
    <a href="/group">
      <div class="info-box bg-green">
        <span class="info-box-icon">
          <i class="fa" v-bind:class="group.class" ></i>
        </span>
        <div class="info-box-content">
          <span class="info-box-number">{{group.name}}</span>
          <span class="info-box-text">{{group.num}} dispositivos</span>
        </div>
        <!-- /.info-box-content -->
      </div>
    </a>
    <!-- /.info-box -->
  </div>
  `
});

