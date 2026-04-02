<template>
  <div class="min-h-screen bg-neutral-50">
    <header class="border-b border-neutral-200 bg-white">
      <UContainer class="relative flex max-w-[1680px] items-center px-10 py-6">
        <UButton
          icon="i-lucide-arrow-left"
          color="neutral"
          variant="soft"
          class="h-8 w-8 justify-center rounded-md"
          :ui="{ leadingIcon: 'm-0' }"
          @click="navigateTo('/')"
        />
        <h1 class="absolute left-1/2 -translate-x-1/2 text-xl font-semibold text-neutral-950">
          新規投稿
        </h1>
      </UContainer>
    </header>

    <main class="px-10 py-10">
      <UContainer class="max-w-[800px]">
        <UCard :ui="{ root: 'rounded-xl border border-neutral-200 bg-white shadow-none', header: 'px-8 py-6', body: 'px-8 py-6', footer: 'px-8 py-6' }">
          <template #header>
            <h2 class="text-xl font-semibold text-neutral-950">投稿を作成</h2>
          </template>

          <form class="space-y-10" @submit.prevent="handleSubmit">
            <div>
              <p class="text-[15px] font-medium text-neutral-950">画像を選択</p>
              <p class="mt-1 text-xs text-neutral-500">JPEG、PNG形式の画像をアップロードできます（最大10MB）</p>

              <label
                class="mt-4 flex h-[200px] cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed border-neutral-200 bg-neutral-50"
              >
                <input type="file" accept="image/*" class="hidden" @change="handleFileChange" />
                <UButton color="neutral" class="mb-5 rounded-lg px-6">ファイルを選択</UButton>
                <p class="text-sm text-neutral-500">または、ここにドラッグ&ドロップ</p>
              </label>

              <div class="mt-6 grid h-[500px] place-items-center rounded-xl border border-dashed border-neutral-200 bg-neutral-100/60">
                <img
                  v-if="previewUrl"
                  :src="previewUrl"
                  alt="画像プレビュー"
                  class="h-full w-full rounded-xl object-cover"
                />
                <div v-else class="text-center">
                  <p class="text-sm text-neutral-500">画像プレビュー</p>
                  <p class="mt-2 text-xs text-neutral-400">画像を選択するとここに表示されます</p>
                </div>
              </div>
            </div>

            <div>
              <p class="text-[15px] font-medium text-neutral-950">キャプション</p>
              <p class="mt-1 text-xs text-neutral-500">投稿に説明文を追加できます（任意）</p>
              <UTextarea
                v-model="caption"
                :rows="7"
                :maxlength="500"
                placeholder="キャプションを入力..."
                class="mt-4"
              />
              <p class="mt-3 text-right text-xs text-neutral-400">{{ caption.length }} / 500</p>
            </div>

            <UAlert
              v-if="statusMessage"
              :color="statusTone"
              variant="soft"
              :title="statusMessage"
            />

            <div class="grid grid-cols-1 gap-4 md:grid-cols-2">
              <UButton
                type="submit"
                color="neutral"
                class="h-12 w-full justify-center rounded-lg"
                :loading="submitting"
              >
                投稿する
              </UButton>
              <UButton
                to="/"
                color="neutral"
                variant="outline"
                class="h-12 w-full justify-center rounded-lg"
              >
                キャンセル
              </UButton>
            </div>
          </form>
        </UCard>
      </UContainer>
    </main>
  </div>
</template>

<script setup lang="ts">
const config = useRuntimeConfig()
const apiBase = config.public.apiBase

const caption = ref('')
const selectedFile = ref<File | null>(null)
const previewUrl = ref('')
const submitting = ref(false)
const statusMessage = ref('')
const statusTone = ref<'error' | 'success'>('success')

const handleFileChange = (event: Event) => {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0] || null
  selectedFile.value = file

  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value)
  }

  previewUrl.value = file ? URL.createObjectURL(file) : ''
  statusMessage.value = ''
}

const handleSubmit = async () => {
  if (!selectedFile.value) {
    statusTone.value = 'error'
    statusMessage.value = '画像を選択してください。'
    return
  }

  submitting.value = true
  statusMessage.value = ''

  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    formData.append('caption', caption.value)

    await $fetch(`${apiBase}/posts`, {
      method: 'POST',
      body: formData,
    })

    statusTone.value = 'success'
    statusMessage.value = '投稿が完了しました。タイムラインへ戻ります。'
    await navigateTo('/')
  } catch (error) {
    console.error(error)
    statusTone.value = 'error'
    statusMessage.value = '投稿に失敗しました。入力内容または API を確認してください。'
  } finally {
    submitting.value = false
  }
}

onBeforeUnmount(() => {
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value)
  }
})
</script>
