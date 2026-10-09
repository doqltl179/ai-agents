---
id: react-native
title: React Native
kind: framework
applies_to: []
related: [react, typescript, kotlin, swift]
volatility: volatile
reviewed: 2026-10-09
sources: ["https://reactnative.dev/docs/getting-started", "https://reactnative.dev/blog", "https://reactnative.dev/architecture/landing-page", "https://docs.expo.dev/", "https://expo.dev/changelog"]
---

# React Native

## Detect
- Expo or bare: an `expo` dependency with `app.json`/`app.config.(js|ts)` means Expo. If `ios/` and `android/` are gitignored, the project uses Continuous Native Generation (CNG, `expo prebuild`); if they are committed, native code is edited in place.
- Versions: `react-native` in `package.json`; in Expo projects the `expo` SDK version decides compatible React Native and library versions.
- Navigation: Expo Router (`expo-router` with an `app/` directory) or React Navigation.
- New Architecture setting: `newArchEnabled` in `app.json` or `android/gradle.properties`, and `RCT_NEW_ARCH_ENABLED` for iOS.
- Metro config (`metro.config.js`), monorepo layout, and `babel.config.js` plugins (for example Reanimated).
- Tests: Jest with the `jest-expo` or `react-native` preset and `@testing-library/react-native`; E2E with Detox or Maestro.

## Conventions
- Build UI from React Native primitives (`View`, `Text`, `Pressable`, `Image`); render every string inside `<Text>`.
- Style with `StyleSheet.create` or the project's styling library; flexbox defaults to `flexDirection: "column"`, and styles do not cascade except text styles into nested `<Text>`.
- Small platform differences: `Platform.OS` or `Platform.select`. Larger ones: `Name.ios.tsx`/`Name.android.tsx` (or `.native.tsx`/`.web.tsx`), imported without the suffix.
- Render long or dynamic lists with `FlatList`/`SectionList` (or the project's list library), never `ScrollView` plus `map`; supply `keyExtractor`, memoized item components, and `getItemLayout` for fixed-height rows.
- Keep native calls behind one typed JS module per capability; write new native modules with the project's approach (Turbo Modules or the Expo Modules API).
- In Expo projects add libraries with `npx expo install <pkg>` so versions match the SDK; in a CNG project change native config through config plugins.
- Treat everything in the JS bundle as public: `EXPO_PUBLIC_*` and other inlined env values are not secrets.
- Respect safe areas (`react-native-safe-area-context`) and the keyboard (`KeyboardAvoidingView`); set `accessibilityLabel` and `accessibilityRole` on custom touchables.

## Verify
- `commands.test`, `commands.lint`, `commands.typecheck`; `commands.e2e` for Detox or Maestro flows.
- Expo: `npx expo-doctor` checks dependency compatibility.
- After native dependency or config changes, rebuild the binary (`npx expo run:ios`/`run:android`, or `pod install` in `ios/` then a native build); a Metro reload is not enough.

## Pitfalls
- Edits to `ios/` or `android/` in a CNG project are lost on the next `npx expo prebuild --clean`; use a config plugin.
- Adding a library with native code and only reloading JavaScript fails with a missing native module; rebuild the app.
- A stale bundler cache after config or dependency changes; restart Metro with `npx expo start -c` or `npx react-native start --reset-cache`.
- Inline object and arrow-function props in `renderItem` of large lists re-render every row; memoize the item component and callbacks.
- Web-only libraries that touch the DOM crash on device; pick libraries that support React Native.
- Upgrading `react-native` alone in an Expo project breaks native compatibility; upgrade the Expo SDK instead.

## Version Notes
- The New Architecture (Fabric, Turbo Modules, bridgeless) is enabled by default since React Native 0.76, and from 0.82 it is the only architecture: `newArchEnabled=false` and `RCT_NEW_ARCH_ENABLED=0` are ignored (as of 2026-10, per reactnative.dev/blog). Check native libraries for New Architecture support before adding them.
- Each Expo SDK targets one React Native version; read its changelog before upgrading (as of 2026-10, per expo.dev/changelog).
