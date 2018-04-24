Vue.component("devicedisplayLight", {
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
  <div class="box box-default">
    <div class="box-header with-border" style="padding:0">
      <div class="info-box bg-green" style="margin:0">
        <span class="info-box-icon">
          <i class="fa fa-lightbulb-o"></i>
        </span>

        <div class="info-box-content">
          <span class="info-box-text">{{device.name}}</span>
          <span class="info-box-number">{{device.id}}</span>
          <span class="pull-right">
            <button type="button" class="btn btn-block btn-primary">
              Apagar/Encender
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
