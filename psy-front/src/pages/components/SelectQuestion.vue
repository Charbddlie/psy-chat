<template>
  <div>
    <div v-for="(q, idx) in questions" :key="idx" class="q-question-block">
      <div class="q-question">
        <span class="q-qindex">{{ idx + 1 }}.</span>
        {{ q.text }}
      </div>
      <div class="q-options">
        <label
          v-for="opt in q.options"
          :key="opt.value"
          :class="['q-option', { selected: modelValue[idx] === opt.value }]"
        >
          <input
            type="radio"
            :value="opt.value"
            :name="'select-' + idx"
            class="q-radio"
            :checked="modelValue[idx] === opt.value"
            @change="$emit('update:modelValue', updateValue(idx, opt.value))"
          />
          <span class="q-option-label">{{ opt.text }}</span>
        </label>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SelectQuestion",
  props: {
    questions: {
      type: Array,
      required: true,
    },
    modelValue: {
      type: Array,
      required: true,
    },
  },
  methods: {
    updateValue(idx, n) {
      // Return a new array with the updated value at idx
      const arr = this.modelValue.slice();
      arr[idx] = n;
      return arr;
    }
  },
};
</script>