Vue.component("menulateral", {
    props: ['current_user'],
    template: `
      <div>
      <header class="main-header">
      <!-- Logo -->
      <a href="/groups" class="logo">
        <!-- mini logo for sidebar mini 50x50 pixels -->
        <span class="logo-mini">
          <b>D</b>Tr</span>
        <!-- logo for regular state and mobile devices -->
        <span class="logo-lg">
          <b>Domotic</b>Trails</span>
      </a>
      <!-- Header Navbar: style can be found in header.less -->
      <nav class="navbar navbar-static-top">
        <a href="#" class="sidebar-toggle" data-toggle="push-menu" role="button">
          <span class="sr-only">Toggle navigation</span>
        </a>
        <div class="navbar-custom-menu">
  
          <ul class="nav navbar-nav">
            <!-- Messages: style can be found in dropdown.less-->
            <!-- User Account: style can be found in dropdown.less -->
            <li class="dropdown user user-menu">
             <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                <span class="hidden-xs">{{current_user}}</span>
              </a>
              <ul class="dropdown-menu">
                <!-- User image -->
                <li class="user-header">
                  <p style="margin-top:25%">
                  {{current_user}}
                  </p>
                </li>
                <!-- Menu Footer-->
                <li class="user-footer">
                  <div class="pull-left">
                      <a href="/changePass" class="btn btn-default btn-flat">Cambiar contraseña</a>
                  </div>
                  <div class="pull-right">
                    <form action="/logout" method="get">
                      <button class="btn btn-default btn-flat" type="submit">Salir</button>
                    </form>
                  </div>
                </li>
              </ul> 
            </li>
          </ul>
        </div>
      </nav>
    </header>
    <!-- Left side column. contains the logo and sidebar -->
    <aside class="main-sidebar">
      <!-- sidebar: style can be found in sidebar.less -->
      <section class="sidebar">
  
        <!-- sidebar menu: : style can be found in sidebar.less -->
        <ul class="sidebar-menu" data-widget="tree">
          <div style="width:50%; margin:auto" class="img-responsive">
            <img src="../../static/DomoticTrails.png" class="img-circle" style="width:100%; margin-top: 15%; margin-bottom: 15%">
          </div>
          <li class="header">CONTROL</li>
          <li class="treeview">
            <a href="#">
              <i class="fa fa-sitemap"></i>
              <span>Grupos</span>
              <span class="pull-right-container">
                <i class="fa fa-angle-left pull-right"></i>
              </span>
            </a>
            <ul class="treeview-menu">
              <li>
                <a href="/groups">
                  <i class="fa fa-circle-o"></i> Ver grupos</a>
              </li>
              <li>
                <a href="/newGroup">
                  <i class="fa fa-circle-o"></i> Añadir grupos</a>
              </li>
            </ul>
          </li>
          <li>
            <a href="/newSensor">
              <i class="fa fa-plus"></i>
              <span>Nuevo dispositivo</span>
            </a>
          </li>
          <li class="treeview">
            <a href="#">
              <i class="fa fa-clock-o"></i>
              <span>Programas</span>
              <span class="pull-right-container">
                <i class="fa fa-angle-left pull-right"></i>
              </span>
            </a>
            <ul class="treeview-menu">
              <li>
                <a href="/programs">
                  <i class="fa fa-circle-o"></i> Ver Programa</a>
              </li>
              <li>
                <a href="/newProgram">
                  <i class="fa fa-circle-o"></i> Añadir programa</a>
              </li>
            </ul>
          </li>
          <li>
            <a href="/manageUserGroups">
              <i class="fa fa-users"></i>
              <span>Usuarios</span>
            </a>
          </li>
          <li class="header">DEBUG</li>
          <li>
            <a href="/newData">
              <i class="fa fa-sliders"></i>
              <span>Añadir medidas manualmente</span>
            </a>
          </li>
        </ul>
      </section>
      <!-- /.sidebar -->
    </aside>
    </div>`,
    methods:{
      logout(){
        socket.emit('logoutUser')
      }
    }
    
  });