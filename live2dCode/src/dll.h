#pragma once
// dll.h
#ifndef DLL_H_
#define DLL_H_

struct Point {
    int x;
    int y;
};

extern "C" _declspec(dllexport) void startLive2d(int x, int y);
extern "C" _declspec(dllexport) Point getPos();
extern "C" _declspec(dllexport) void closeLive2d();
extern "C" _declspec(dllexport) bool isLeftTouch();
extern "C" _declspec(dllexport) bool isRightTouch();
extern "C" _declspec(dllexport) bool isOK();

#endif