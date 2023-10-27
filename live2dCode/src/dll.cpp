
#include <windows.h>
#include <iostream>
#include "LAppDelegate.hpp"
#include "LAppLive2DManager.hpp"
#include "dll.h"

//dll.cpp
extern "C" _declspec(dllexport)void startLive2d(int x,int y)
{
    // アプリケーション初期化
    if (!LAppDelegate::GetInstance()->Initialize(x,y))
    {// 初期化失敗
        LAppDelegate::GetInstance()->Release();
        LAppDelegate::ReleaseInstance();
        std::cerr << "Initialization failed." << std::endl;
        return;
    }
    std::cout << "Initialization ok." << std::endl;
    LAppDelegate::GetInstance()->Run();
}

extern "C" _declspec(dllexport) Point getPos() {
    LAppDelegate* ins = LAppDelegate::GetInstance();
    HWND hwnd = ins->_hw;  // 替换为你的窗口句柄

    // 获取窗口矩形区域
    RECT windowRect;
    GetWindowRect(hwnd, &windowRect);

    Point center;
    center.x = (windowRect.left + windowRect.right) / 2;
    center.y = (windowRect.top + windowRect.bottom) / 2;

    return center;
}
extern "C" _declspec(dllexport) void closeLive2d() {
    LAppDelegate* ins = LAppDelegate::GetInstance();
    ins->isFinished = true;

}
extern "C" _declspec(dllexport) bool isLeftTouch(){
    if (LAppLive2DManager::GetInstance()->isLeftTouch)
    {
		LAppLive2DManager::GetInstance()->isLeftTouch = false;
		return true;
	}
    return false;
}

extern "C" _declspec(dllexport) bool isRightTouch() {
    if (LAppLive2DManager::GetInstance()->isRightTouch)
    {
        LAppLive2DManager::GetInstance()->isRightTouch = false;
        return true;
    }
    return false;
}
extern "C" _declspec(dllexport) bool isOK(){
    LAppDelegate* ins = LAppDelegate::GetInstance();
    return ins->isOK;
}
