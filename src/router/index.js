import { createRouter, createWebHistory } from 'vue-router'
import RegistrationView from '../views/RegistrationView.vue'
import ProfileView from '@/views/ProfileView.vue'
import DashboardView from '@/views/DashboardView.vue'
import TrainingView from '@/views/TrainingView.vue'
import ServingView from '@/views/ServingView.vue'
import ModelManageView from '@/views/ModelManageView.vue'
import DataListView from '@/views/DataListView.vue'
import DatasetDetails from '@/views/DatasetDetails.vue'

const routes = [
  {
    path: '/',
    name: 'regristation',
    component: RegistrationView
  },
  {
    path: '/profile',
    name: 'Profile',
    component: ProfileView
  },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: DashboardView
  },
  {
    path: '/training',
    name: 'Training',
    component: TrainingView
  },
  {
    path: '/serving',
    name: 'Serving',
    component: ServingView
  },
  {
    path: '/models',
    name: 'Models',
    component: ModelManageView
  },
  {
    path: '/datasetslibrary',
    name: 'DatasetsLibrary',
    component: DataListView
  },
  {
    path: '/dataset/:id',
    name: 'DatasetDetails',
    component: DatasetDetails
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
