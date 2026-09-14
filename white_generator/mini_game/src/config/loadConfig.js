import defaultConfig from './defaultConfig.json';

function deepMerge(base, override) {
  const result = { ...base };
  for (const key in override) {
    if (
      override[key] &&
      typeof override[key] === 'object' &&
      !Array.isArray(override[key]) &&
      base[key] &&
      typeof base[key] === 'object'
    ) {
      result[key] = deepMerge(base[key], override[key]);
    } else {
      result[key] = override[key];
    }
  }
  return result;
}

export async function loadConfig() {
  let userConfig = null;

  if (typeof window !== 'undefined' && window.__CONFIG__) {
    userConfig = window.__CONFIG__;
  } else {
    try {
      const res = await fetch('./config.json');
      if (res.ok) userConfig = await res.json();
    } catch (e) {
    }
  }

  return userConfig ? deepMerge(defaultConfig, userConfig) : defaultConfig;
}