Vue.component("devicedisplaySensor", {
  props: ['devices'],
  template:
  `
  <div>
  <deviceInfoBox
    v-for="device in devices"
    v-bind:key="device.disID"
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
  <div class="box box-default expanded-box">
    <div class="box-header with-border" style="padding:0">
      <div class="info-box bg-green" style="margin:0">
        <span class="info-box-icon">
          <i class="fa fa-lightbulb-o"></i>
        </span>

        <div class="info-box-content">
          <span class="info-box-text">{{device.name}}</span>
          <span class="info-box-number">{{device.id}}</span>
        </div>
        <!-- /.info-box-content -->
      </div>

      <div class="box-tools pull-right">
        <button type="button" class="btn btn-box-tool" data-widget="collapse">
          <i class="fa fa-minus" style="color:grey"></i>
        </button>
      </div>
      <!-- /.box-tools -->
    </div>
    <!-- /.box-header -->
    <div class="box-body" id="collapsable">
      <div class="box box-primary">
        <div class="box-header with-border">
          <h3 class="box-title">Gráfico</h3>

          <div class="box-tools pull-right">
          </div>
        </div>
        <div class="box-body">
          <div class="chart">
            <canvas id="areaChart" style="height:250px"></canvas>
          </div>
        </div>
        <!-- /.box-body -->
      </div>
    </div>
    <!-- /.box-body -->
  </div>
  </div>

  `
});
