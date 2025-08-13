import { createRouter, createWebHistory } from 'vue-router'
import RegistrationView from '../views/RegistrationView.vue'
import ProfileView from '@/views/ProfileView.vue'
import DashboardView from '@/views/DashboardView.vue'
import TrainingView from '@/views/TrainingView.vue'
import ServingView from '@/views/ServingView.vue'
import ModelListView from '@/views/ModelListView.vue'
import DataListView from '@/views/DataListView.vue'
import DatasetDetails from '@/views/DatasetDetails.vue'
import UsersManagement from '@/views/UsersManagement.vue'
import AddUser from '@/views/AddUser.vue'
import UploadDataset from '@/views/UploadDataset.vue'
import ModelDetails from '@/views/ModelDetails.vue'

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
    component: ModelListView
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
  },
  {
    path: '/users',
    name: 'UsersManagement',
    component: UsersManagement
  },
  {
    path: "/addUser",
    name: "AddUser",
    component: AddUser
  },
  {
    path: "/uploadDataset",
    name: "UploadDataset",
    component: UploadDataset
  },
  {
    path: "/model/:id",
    name: "ModelDetails",
    component: ModelDetails
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
