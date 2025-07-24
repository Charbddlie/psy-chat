<template>
  <div>
    <div
      class="q-question-block"
      v-for="(q, idx) in questions"
      :key="q.id || idx"
    >
      <div class="q-question">
        <span class="q-qindex">{{ idx + 1 }}.</span>
        {{ q.text }}
      </div>
      <div class="q-scale">
        <span class="q-scale-label">1</span>
        <div class="q-scale-options">
          <label
            v-for="n in max"
            :key="n"
            :class="['q-scale-item', { selected: modelValue[idx] === n }]"
          >
            <input
              type="radio"
              :value="n"
              :name="'scale-' + idx"
              class="q-scale-radio"
              :checked="modelValue[idx] === n"
              @change="$emit('update:modelValue', updateValue(idx, n))"
            />
            <span>{{ n }}</span>
          </label>
        </div>
        <span class="q-scale-label">{{ max }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ScaleQuestion",
  props: {
    questions: {
      type: Array,
      required: true,
    },
    max: {
      type: Number,
      default: 5,
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
