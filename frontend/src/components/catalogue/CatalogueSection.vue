<template>
  <div>
    <!-- Formulaire d'ajout -->
    <form @submit.prevent="submit" class="card p-4 mb-5 flex flex-wrap gap-3 items-end">
      <div v-for="champ in champs" :key="champ" class="flex-1 min-w-32">
        <label class="block text-xs font-medium text-gray-600 mb-1 capitalize">{{ champ }}</label>
        <input v-model="form[champ]" :required="champ === 'nom'" class="input text-sm" :placeholder="champ" />
      </div>
      <div v-if="extra" class="flex-1 min-w-32">
        <label class="block text-xs font-medium text-gray-600 mb-1">{{ extra.label }} *</label>
        <select v-model="form[extra.key]" class="input text-sm" required>
          <option disabled value="">Choisir</option>
          <option v-for="o in extra.options" :key="o.id" :value="o.id">{{ o.nom }}</option>
        </select>
      </div>
      <button type="submit" class="btn-primary text-sm py-2 shrink-0">+ Ajouter</button>
    </form>

    <!-- Liste -->
    <div v-if="loading" class="text-center text-gray-400 py-6">Chargement…</div>
    <div v-else-if="items.length === 0" class="text-center text-gray-400 py-6">Aucun élément.</div>
    <div v-else class="card overflow-hidden">
      <table class="w-full text-sm">
        <thead class="bg-gray-50 border-b border-gray-200">
          <tr>
            <th v-for="champ in champs" :key="champ" class="text-left px-4 py-3 font-medium text-gray-600 capitalize">{{ champ }}</th>
            <th v-if="extra" class="text-left px-4 py-3 font-medium text-gray-600">{{ extra.label }}</th>
            <th class="px-4 py-3"></th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="item in items" :key="item.id" class="hover:bg-gray-50">
            <td v-for="champ in champs" :key="champ" class="px-4 py-3 text-gray-700">{{ item[champ] || '—' }}</td>
            <td v-if="extra" class="px-4 py-3 text-gray-500">
              {{ extra.options.find(o => o.id === item[extra.key])?.nom || item[extra.key] || '—' }}
            </td>
            <td class="px-4 py-3 text-right">
              <button @click="$emit('delete', item.id)" class="text-red-500 hover:text-red-700 text-xs px-2 py-1 rounded hover:bg-red-50">
                Supprimer
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'

const props = defineProps({
  titre: String,
  items: { type: Array, default: () => [] },
  champs: { type: Array, default: () => ['nom'] },
  extra: { type: Object, default: null },
  loading: Boolean,
})
const emit = defineEmits(['create', 'delete'])

const form = reactive({})
props.champs.forEach(c => { form[c] = '' })
if (props.extra) form[props.extra.key] = ''

function submit() {
  emit('create', { ...form })
  props.champs.forEach(c => { form[c] = '' })
  if (props.extra) form[props.extra.key] = ''
}
</script>
