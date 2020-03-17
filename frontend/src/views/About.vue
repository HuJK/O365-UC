<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <div class="d-flex align-center">
        <v-img
          alt="Vuetify Logo"
          class="shrink mr-2"
          contain
          src="https://blobs.officehome.msocdn.com/images/content/images/favicon-8f211ea639.ico"
          transition="scale-transition"
          width="40"
        />
      </div>

      <v-spacer></v-spacer>

      <v-btn icon color="grey lighten-2" to="/admin">
        <v-icon>mdi-cog</v-icon>
        </v-btn>
    </v-app-bar>

  </v-app>
</template>
