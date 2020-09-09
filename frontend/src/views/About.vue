<template>
  <v-app>
    <p>{{a}}</p>
    <p>{{b}}</p>
  </v-app>
</template>

<script>

export default {

  components: {
  },

  data: () => ({
    //
  }),
  computed:{
    a(){return atob("QXV0aG9yOiBIdUpL")},
    b(){return atob("U291cmNlIENvZGU6IGh0dHBzOi8vZ2l0aHViLmNvbS9IdUpLL08zNjUtVUM=")}
  }
};
</script>
