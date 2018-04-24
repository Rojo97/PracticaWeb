Vue.component("devicedisplay", {
  props: ['devices'],
  template:
  `
  <div>
  <deviceInfoBox
    v-for="device in devices"
    v-bind:key="device.id"
    v-bind:device="device"
  ></deviceInfoBox>
  </div>
  `
});
Vue.component("deviceInfoBox", {
  props:["device"],
  template:
  `
  <div style="margin-bottom:2%; margin-left:10%; margin-right:15%">
  <div class="info-box bg-green">
    <span class="info-box-icon">
      <i class="fa" v-bind:class="device.class" ></i>
    </span>
    <div class="info-box-content">
      <span class="info-box-number">{{device.name}}</span>
      <span class="info-box-text">{{device.id}} dispositivos</span>
    </div>
    <!-- /.info-box-content -->
  </div>
    <!-- /.info-box -->
  </div>
  `
});
