Vue.component("devicedisplaysensor", {
  props: ['devices'],
  template:
    `
  <div>
  <deviceInfoBoxSensor
    v-for="device in devices"
    v-bind:key="device.id"
    v-bind:device="device"
    @add-value="$emit('add-sensor-value', { deviceId: device.id, value: $event})"
  ></deviceInfoBoxSensor>
  </div>
  `
});
Vue.component("deviceInfoBoxSensor", {
  props: ["device"],
  template:
    `
  <div style="margin-bottom:2%; margin-left:10%; margin-right:15%"
  v-if = "device.tipo === 'Sensor'">
  <div class="box box-default expanded-box">
    <div class="box-header with-border" style="padding:0">
      <div class="info-box bg-green" style="margin:0">
        <span class="info-box-icon">
          <i class="fa fa-lightbulb-o"></i>
        </span>

        <div class="info-box-content">
          <span class="info-box-text">{{device.name}}</span>
          <span class="info-box-number">{{lastMeassurement}}</span>
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
          <line-chart :chartData="chartData" v-if="device.meassurements.length"></line-chart>
          <div class="well" v-else>El sensor no tiene medidas</div>
        </div>
        <!-- /.box-body -->
      </div>
    </div>
    <!-- /.box-body -->
  </div>
  </div>

  `,
  data: function () {
    return {
      label: 'Temperature',
    }
  },
  computed: {
    chartData() {
      return {
        labels: this.labels,
        datasets: [
          {
            label: this.label,
            data: this.values,
            fill: false,
            stepped: true,
            tension: 0
          }
        ]
      };
    },
    lastMeassurement() {
      return this.sortedMeassurements.length ? this.sortedMeassurements[this.sortedMeassurements.length - 1].value : '--';
    },
    sortedMeassurements() {
      return this.device.meassurements.sort((meassurementA, meassurementB) => {
        return meassurementA.date > meassurementB.date;
      })
    },
    labels() {
      return this.sortedMeassurements.map(meassurement => meassurement.date.toLocaleDateString("es"));
    },
    values() {
      return this.sortedMeassurements.map(meassurement => meassurement.value);
    }
  }
});
Vue.component("line-chart", {
  extends: VueChartJs.Line,
  mixins: [VueChartJs.mixins.reactiveProp],
  props: ['chartData'],
  mounted() {
    this.renderChart(this.chartData, { responsive: true, maintainAspectRatio: false })
  }
});
