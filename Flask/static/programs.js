Vue.component("programdisplay", {
  props: ['programs','grupoamostrar'],
  template:
  `
  <div>
  <programinfobox
    v-for="program in programs"
    v-if="program.group == grupoamostrar || grupoamostrar == 'Todos los grupos'"
    v-bind:key="program.id"
    v-bind:program="program"
  ></programinfobox>
  </div>
  `
});

Vue.component("deviceprogramdisplay", {
  props: ['programs','tipo','funcion'],
  template:
  `
  <ul>
<li v-for="program in programs"
  v-if="program.funcion == funcion">
  {{program.nameP}} -
  [{{program.horaIni}},
  {{program.horaFin}}]
  <i class="fa fa-trash" style="color:red">
  </li>
  </ul>
  `
});

Vue.component("programinfobox", {
  props:['program'],
  template:
  `
  <div class="box box-default">
          <div class="box-header with-border" style="padding:0">
            <div class="info-box bg-green" style="margin:0">
              <span class="info-box-icon">
                <i class="fa" :class="program.class"></i>
              </span>

              <div class="info-box-content">
                <span class="info-box-number">{{program.name}}</span>
                <span class="info-box-text">
                  <small>{{program.group}}</small>
                </span>
              </div>
              <!-- /.info-box-content -->
            </div>

            <div class="box-tools pull-right">
              <button type="button" class="btn btn-box-tool" data-widget="collapse">
                <i class="fa fa-plus" style="color:grey"></i>
              </button>
            </div>
            <!-- /.box-tools -->
          </div>
          <!-- /.box-header -->
          <div class="box-body" style="display: none; margin-top:2%">
            <div class="row">
              <div class="col-md-3" style="margin-left:7%">
                <strong>
                  <i class="fa"></i>
                  <big>Luces</big>
                </strong>
                <p class="text-muted">
                <deviceprogramdisplay v-bind:programs="program.subprograms" v-bind:funcion="'Luminosidad'"></deviceprogramdisplay>
                </p>
              </div>
              <div class="col-md-3">
                <strong>
                  <i class="fa"></i>
                  <big>Persianas</big>
                </strong>
                <p class="text-muted">
                <deviceprogramdisplay v-bind:programs="program.subprograms" v-bind:funcion="'Persianas'"></deviceprogramdisplay>
                </p>
              </div>
              <div class="col-md-3">
                <strong>
                  <i class="fa"></i>
                  <big>Termostatos</big>
                </strong>
                <p class="text-muted">
                <deviceprogramdisplay v-bind:programs="program.subprograms" v-bind:funcion="'Temperatura'"></deviceprogramdisplay>
                </p>
              </div>
              <hr>
            </div>
            <button type="submit" class="btn btn-default">Eliminar</button>
            <button type="submit" class="btn btn-info pull-right bg-green">Editar</button>
          </div>
          <!-- /.box-body -->
        </div>
  `
});
