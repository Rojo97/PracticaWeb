Vue.component("devicedisplaylight", {
  props: ['devices'],
  template:
  `
  <div>
  <deviceInfoBoxLight
    v-for="device in devices"
    v-bind:key="device.id"
    v-bind:device="device"
  ></deviceInfoBoxLight>
  </div>
  `
});
Vue.component("deviceInfoBoxLight", {
  props:["device"],
  template:
  `
  <div style="margin-bottom:2%; margin-left:10%; margin-right:15%"
  v-if = "device.tipo === 'Actuador' && device.funcion === 'Luminosidad'">
  <div class="box box-default">
    <div class="box-header with-border" style="padding:0">
      <div class="info-box bg-green" style="margin:0">
        <span class="info-box-icon">
          <i class="fa fa-lightbulb-o"></i>
        </span>

        <div class="info-box-content">
          <span class="info-box-text">{{device.name}}</span>
          <span v-if = "device.estado === 0" class="info-box-number">Apagada</span>
          <span v-else class="info-box-number">Encendida</span>
          <span class="pull-right">
            <button v-if = "device.estado === 0" type="button" class="btn btn-block btn-primary">
              Encender
            </button>
            <button v-else type="button" class="btn btn-block btn-primary">
              Apagar
            </button>
          </span>
        </div>
        <!-- /.info-box-content -->


      </div>
      <!-- /.box-tools -->
    </div>
    <!-- /.box-header -->
    <div class="box-body" style="display: none;">
    </div>
    <!-- /.box-body -->
  </div>
  </div>

  `
});
