<template>
  <div class="min-h-screen bg-neutral-50">
    <header class="border-b border-neutral-200 bg-white">
      <UContainer class="flex max-w-[1680px] items-center justify-between px-10 py-6">
        <h1 class="text-2xl font-bold text-neutral-950">Instagram Clone</h1>
        <UButton
          to="/post/new"
          icon="i-lucide-plus"
          size="xl"
          class="h-14 w-14 justify-center rounded-full"
          :ui="{ leadingIcon: 'm-0' }"
        />
      </UContainer>
    </header>

    <main class="px-10 py-10">
      <UContainer class="max-w-[1680px]">
        <div v-if="pending" class="grid grid-cols-1 gap-10 lg:grid-cols-3">
          <UCard v-for="item in 6" :key="item" :ui="cardUi">
            <template #header>
              <div class="flex items-center gap-3">
                <USkeleton class="h-9 w-9 rounded-full" />
                <div class="space-y-2">
                  <USkeleton class="h-4 w-20" />
                  <USkeleton class="h-3 w-28" />
                </div>
              </div>
            </template>
            <USkeleton class="aspect-square w-full rounded-none" />
            <template #footer>
              <div class="space-y-2">
                <USkeleton class="h-4 w-20" />
                <USkeleton class="h-4 w-full" />
              </div>
            </template>
          </UCard>
        </div>

        <div v-else-if="error" class="flex min-h-[60vh] items-center justify-center">
          <UCard class="w-full max-w-md" :ui="{ body: 'text-center space-y-4', footer: 'justify-center' }">
            <template #header>
              <div class="text-center">
                <h2 class="text-lg font-semibold text-neutral-950">エラーが発生しました</h2>
              </div>
            </template>
            <p class="text-sm text-neutral-600">投稿の取得に失敗しました。</p>
            <p class="text-sm text-neutral-500">ネットワークエラーが発生した可能性があります。</p>
            <template #footer>
              <UButton color="neutral" @click="refresh()">再試行</UButton>
            </template>
          </UCard>
        </div>

        <div v-else-if="!posts || posts.length === 0" class="flex min-h-[60vh] items-center justify-center">
          <div class="text-center">
            <div class="mx-auto mb-6 grid h-20 w-20 place-items-center rounded-lg border border-neutral-200 bg-neutral-100">
              <UIcon name="i-lucide-image" class="h-9 w-9 text-neutral-400" />
            </div>
            <p class="text-lg text-neutral-500">まだ投稿がありません</p>
            <p class="mt-2 text-sm text-neutral-400">最初の投稿を作成して、みんなとシェアしましょう</p>
            <UButton to="/post/new" color="neutral" class="mt-8 h-12 rounded-lg px-6">
              最初の投稿を作成
            </UButton>
          </div>
        </div>

        <div v-else class="grid grid-cols-1 gap-10 lg:grid-cols-3">
          <UCard
            v-for="post in posts"
            :key="post.id"
            :ui="cardUi"
          >
            <template #header>
              <div class="flex items-center gap-3">
                <UAvatar :text="avatarInitial" size="md" />
                <div>
                  <p class="text-sm font-semibold text-neutral-950">User</p>
                  <p class="text-xs text-neutral-500">{{ formatDate(post.created_at) }}</p>
                </div>
              </div>
            </template>

            <img
              :src="post.image_url"
              :alt="post.caption || '投稿画像'"
              class="aspect-square w-full object-cover"
            />

            <template #footer>
              <div class="space-y-2">
                <p class="text-sm font-semibold text-neutral-950">User</p>
                <p class="text-sm text-neutral-950">{{ post.caption || '' }}</p>
              </div>
            </template>
          </UCard>
        </div>
      </UContainer>
    </main>
  </div>
</template>

<script setup lang="ts">
type Post = {
  id: number
  image_url: string
  caption: string | null
  created_at: string
}

const cardUi = {
  root: 'overflow-hidden rounded-xl border border-neutral-200 bg-white shadow-none',
  header: 'px-4 py-4',
  body: 'p-0',
  footer: 'px-4 py-4',
}

const config = useRuntimeConfig()
const apiBase = config.public.apiBase

const {
  data: posts,
  pending,
  error,
  refresh,
} = await useFetch<Post[]>(`${apiBase}/posts`, {
  default: () => [],
})

const formatDate = (value: string) =>
  new Intl.DateTimeFormat('ja-JP', {
    year: 'numeric',
    month: 'numeric',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(value))

const avatarInitial = 'U'

onMounted(() => {
  refresh()
})
</script>
