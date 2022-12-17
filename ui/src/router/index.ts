import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import CardView from "@/views/CardView.vue";
import IdolView from "@/views/IdolView.vue";
import HistoryView from "@/views/HistoryView.vue";
import NotFoundView from "@/views/NotFoundView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/history/:page(\\d+)",
      name: "history",
      component: HistoryView
    },
    {
      path: "/card/:id(\\d+)",
      name: "card",
      component: CardView,
    },
    {
      path: "/idol/:id(\\d+)",
      name: "idol",
      component: IdolView
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: NotFoundView
    }
  ],
});

export default router;
