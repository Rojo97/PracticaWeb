Vue.component("devicedisplay", {
  props: ['devices'],
  template:
  `
  <div>
  <deviceInfoBoxNormal
    v-for="device in devices"
    v-bind:key="device.id"
    v-bind:device="device"
  ></deviceInfoBoxNormal>
  </div>
  `
});
Vue.component("deviceInfoBoxNormal", {
  props:["device"],
  template:
  `
  <div style="margin-bottom:2%; margin-left:10%; margin-right:15%"
  v-if = "device.tipo === 'Actuador' && device.funcion !== 'Luminosidad'">
  <div class="info-box bg-green">
    <span class="info-box-icon">
      <i v-if = "device.funcion === 'Temperatura'" class="fa fa-eyedropper"></i>
      <i v-else class="fa fa-sun-o"></i>
    </span>
    <div class="info-box-content">
      <span class="info-box-number">{{device.name}}</span>
      <div v-if = "device.funcion === 'Persiana'">
      <span class="info-box-text">{{device.estado}}</span>
      <span class="pull-right">
        <div v-if = "device.estado > 0.5">
        <button type="button" class="btn btn-block btn-primary">
          Bajar
        </button>
        </div>
        <div v-else>
        <button v-else type="button" class="btn btn-block btn-primary">
          Subir
        </button>
        </div>
      </span>
      </div>
      <div v-else>
      <span class="info-box-text">{{device.estado}} ºC</span>
      </div>
    </div>
    <!-- /.info-box-content -->
  </div>
    <!-- /.info-box -->
  </div>
  `
});
