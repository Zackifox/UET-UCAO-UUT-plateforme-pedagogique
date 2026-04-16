<template>
  <div class="max-w-5xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold text-gray-900 mb-6">Gestion du catalogue</h1>

    <!-- Onglets -->
    <div class="flex gap-1 mb-6 border-b border-gray-200">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        @click="activeTab = tab.key"
        class="px-4 py-2 text-sm font-medium border-b-2 transition-colors -mb-px"
        :class="activeTab === tab.key ? 'border-blue-700 text-blue-700' : 'border-transparent text-gray-500 hover:text-gray-800'"
      >
        {{ tab.label }}
      </button>
    </div>

    <!-- Instituts -->
    <div v-if="activeTab === 'instituts'">
      <CatalogueSection
        titre="Instituts"
        :items="instituts"
        :champs="['nom', 'sigle', 'description']"
        :loading="loading"
        @create="createInstitut"
        @delete="deleteInstitut"
      />
    </div>

    <!-- Filières -->
    <div v-if="activeTab === 'filieres'">
      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 mb-1">Filtrer par Institut</label>
        <select v-model="filtreInstitut" @change="loadFilieres" class="input max-w-xs text-sm">
          <option value="">Tous</option>
          <option v-for="i in instituts" :key="i.id" :value="i.id">{{ i.sigle || i.nom }}</option>
        </select>
      </div>
      <CatalogueSection
        titre="Filières"
        :items="filieres"
        :champs="['nom', 'sigle', 'description']"
        :extra="{ label: 'Institut', key: 'institut', options: instituts }"
        :loading="loading"
        @create="createFiliere"
        @delete="deleteFiliere"
      />
    </div>

    <!-- Niveaux -->
    <div v-if="activeTab === 'niveaux'">
      <div class="mb-4 flex gap-3 flex-wrap">
        <select v-model="filtreInstitut" @change="loadFilieres" class="input max-w-xs text-sm">
          <option value="">Tous les instituts</option>
          <option v-for="i in instituts" :key="i.id" :value="i.id">{{ i.sigle || i.nom }}</option>
        </select>
        <select v-model="filtreFiliere" @change="loadNiveaux" class="input max-w-xs text-sm" :disabled="!filieres.length">
          <option value="">Toutes les filières</option>
          <option v-for="f in filieres" :key="f.id" :value="f.id">{{ f.nom }}</option>
        </select>
      </div>
      <CatalogueSection
        titre="Niveaux"
        :items="niveaux"
        :champs="['nom', 'ordre']"
        :extra="{ label: 'Filière', key: 'filiere', options: filieres }"
        :loading="loading"
        @create="createNiveau"
        @delete="deleteNiveau"
      />
    </div>

    <!-- Matières -->
    <div v-if="activeTab === 'matieres'">
      <div class="mb-4 flex gap-3 flex-wrap">
        <select v-model="filtreFiliere" @change="loadNiveaux" class="input max-w-xs text-sm">
          <option value="">Toutes les filières</option>
          <option v-for="f in filieres" :key="f.id" :value="f.id">{{ f.nom }}</option>
        </select>
        <select v-model="filtreNiveau" @change="loadMatieres" class="input max-w-xs text-sm" :disabled="!niveaux.length">
          <option value="">Tous les niveaux</option>
          <option v-for="n in niveaux" :key="n.id" :value="n.id">{{ n.nom }}</option>
        </select>
      </div>
      <CatalogueSection
        titre="Matières"
        :items="matieres"
        :champs="['nom', 'code', 'description']"
        :extra="{ label: 'Niveau', key: 'niveau', options: niveaux }"
        :loading="loading"
        @create="createMatiere"
        @delete="deleteMatiere"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, defineAsyncComponent } from 'vue'
import { catalogueApi } from '@/api/catalogue'

const CatalogueSection = defineAsyncComponent(() => import('@/components/catalogue/CatalogueSection.vue'))

const tabs = [
  { key: 'instituts', label: 'Instituts' },
  { key: 'filieres', label: 'Filières' },
  { key: 'niveaux', label: 'Niveaux' },
  { key: 'matieres', label: 'Matières' },
]
const activeTab = ref('instituts')
const loading = ref(false)
const instituts = ref([])
const filieres = ref([])
const niveaux = ref([])
const matieres = ref([])
const filtreInstitut = ref('')
const filtreFiliere = ref('')
const filtreNiveau = ref('')

onMounted(async () => {
  const { data } = await catalogueApi.getInstituts()
  instituts.value = data.results || data
  const fData = await catalogueApi.getFilieres()
  filieres.value = fData.data.results || fData.data
})

async function loadFilieres() {
  filtreFiliere.value = ''; niveaux.value = []; matieres.value = []
  const params = filtreInstitut.value ? { institut: filtreInstitut.value } : {}
  const { data } = await catalogueApi.getFilieres(params)
  filieres.value = data.results || data
}

async function loadNiveaux() {
  filtreNiveau.value = ''; matieres.value = []
  const params = filtreFiliere.value ? { filiere: filtreFiliere.value } : {}
  const { data } = await catalogueApi.getNiveaux(params)
  niveaux.value = data.results || data
}

async function loadMatieres() {
  const params = filtreNiveau.value ? { niveau: filtreNiveau.value } : {}
  const { data } = await catalogueApi.getMatieres(params)
  matieres.value = data.results || data
}

async function createInstitut(d) { const r = await catalogueApi.createInstitut(d); instituts.value.push(r.data) }
async function deleteInstitut(id) { await catalogueApi.deleteInstitut(id); instituts.value = instituts.value.filter(i => i.id !== id) }
async function createFiliere(d) { const r = await catalogueApi.createFiliere(d); filieres.value.push(r.data) }
async function deleteFiliere(id) { await catalogueApi.deleteFiliere(id); filieres.value = filieres.value.filter(i => i.id !== id) }
async function createNiveau(d) { const r = await catalogueApi.createNiveau(d); niveaux.value.push(r.data) }
async function deleteNiveau(id) { await catalogueApi.deleteNiveau(id); niveaux.value = niveaux.value.filter(i => i.id !== id) }
async function createMatiere(d) { const r = await catalogueApi.createMatiere(d); matieres.value.push(r.data) }
async function deleteMatiere(id) { await catalogueApi.deleteMatiere(id); matieres.value = matieres.value.filter(i => i.id !== id) }
</script>
