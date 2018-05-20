Vue.component("usergroupdisplay", {
  props: ['usergroups'],
  template:
  `
  <div>
  <groupuserinfobox
    v-for="usergroup in usergroups"
    v-bind:key="usergroup.id"
    v-bind:groupuser="usergroup"
  ></groupuserinfobox>
  </div>
  `
});
Vue.component("groupuserinfobox", {
  props:["groupuser"],
  template:
  `
  <div style="margin-right:15%; margin-left:15%">
  <div class="box box-default">
    <div class="box-header with-border" style="padding:0">
      <div class="info-box bg-green" style="margin:0">
        <span class="info-box-icon">
        </span>

        <div class="info-box-content">
          <span class="info-box-number">{{groupuser.name}}</span>
          <span class="info-box-text">
          <span class="info-box-text">{{groupuser.num}} usuarios</span>
            <small>{{groupuser.desc}}</small>
          </span>
        </div>
        <!-- /.info-box-content -->
      </div>

      <div class="box-tools pull-right">
        <button type="button" class="btn btn-box-tool" data-widget="collapse">
          <i class="fa fa-plus" style="color:white"></i>
        </button>
      </div>
      <!-- /.box-tools -->
    </div>
    <!-- /.box-header -->
    <div class="box-body" style="display: none; margin-top:2%">
      <div style="padding-left:10%; padding-right:10%">
      <strong>
        <i class="fa"></i>
        <big>Usuarios</big>
      </strong>

      <ul>
        <userdisplay v-bind:users="users"></userdisplay>
      </ul>
    </div>
      <button type="submit" class="btn btn-default pull-right bg-green">Añadir usuario</button>
    </div>
    <!-- /.box-body -->
  </div>
</div>
  `
});

