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
    v-bind:subprograms="program.subprogramas"
  ></programinfobox>
  </div>
  `
});

Vue.component("deviceprogramdisplay", {
  props: ['programs','tipo','funcion'],
  template:
  `
  <div>
  <p
    v-for="program in programs"
    v-if="program.tipo == tipo || program.funcion == funcion"
    <li>{{program.nombre}}</li>
  ></p>
  </div>
  `
});

Vue.component("programinfobox", {
  props:["program"],
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
              <div class="col-md-2" style="margin-left:7%">
                <strong>
                  <i class="fa"></i>
                  <big>Luces</big>
                </strong>
                <deviceprogramdisplay v-bind:programs={{program.subprogramas}} v-bind:tipo='Actuador' v-bind:funcion='Luminosidad'>
              </div>
              <div class="col-md-2">
                <strong>
                  <i class="fa"></i>
                  <big>Persianas</big>
                </strong>

                <p class="text-muted">
                  <ul>
                    <li>Persiana 1</li>
                    <li>Persiana 2</li>
                  </ul>
                </p>
              </div>
              <div class="col-md-2">
                <strong>
                  <i class="fa"></i>
                  <big>Termostatos</big>
                </strong>

                <p class="text-muted">
                  <ul>
                    <li>Termostato 1</li>
                  </ul>
                </p>
              </div>
              <div class="col-md-2">
                <strong>
                  <i class="fa"></i>
                  <big>Sensores luminosidad</big>
                </strong>

                <p class="text-muted">
                  <ul>
                    <li>Luminosidad 1</li>
                    <li>Luminosidad 2</li>
                  </ul>
                </p>
              </div>
              <div class="col-md-2">
                <strong>
                  <i class="fa"></i>
                  <big>Termometros</big>
                </strong>

                <p class="text-muted">
                  <ul>
                    <li>Termometro 1</li>
                  </ul>
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
