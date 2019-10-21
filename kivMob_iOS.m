"""
Objective-C script for AdMob ads implementation in iOS based applications. Its major application is with the Kivy library. This code is to be run from the xcode project after kivy translation.
Copy and paste the script in the main.m file just below #import <Firebase/Firebase.h>

The current script implements banners and interstitial ads. Soon to be implemented are reward videos.

By Alessio Tamborini
"""

UIView *gView;
UIViewController *gViewColtroller;

@interface myBanner : NSObject <GADBannerViewDelegate>
@property (nonatomic) BOOL show_ads_banner;
@property (strong, nonatomic) GADBannerView *gbanner;
@property (strong, nonatomic) GADRequest *request;
@end

static myBanner *vbanner = nil;

@implementation myBanner

-(id)init {
    
    NSLog(@"Creating google banner object");
    self.request = [GADRequest request];
    
    UIWindow *window = [UIApplication sharedApplication].keyWindow;
    UIViewController *rootViewController = window.rootViewController;
    
    gViewColtroller = rootViewController;//[[SDLLaunchScreenController alloc] init];
    gView = rootViewController.view; ///gViewColtroller.view;
    
    self.gbanner = [[GADBannerView alloc] initWithAdSize:kGADAdSizeBanner]; // Create a view of the standard size at the top of the screen, Available AdSize constants are explained in GADAdSize.h.
    [self.gbanner setDelegate:self];
    
//    self.gbanner.adUnitID = @"ca-app-pub-3940256099942544/6300978111"; // google's test id for banner ads
    self.gbanner.adUnitID = @"ca-app-pub-8564280870740386/7580629478"; //my id for the banner ads
    
    //  ------------- Height and position of the banner ad
    CGRect screenBounds = [[UIScreen mainScreen] bounds];
    self.gbanner.center = CGPointMake(screenBounds.size.width / 2, screenBounds.size.height - (self.gbanner.bounds.size.height / 2));
    
    self.gbanner.hidden = TRUE;
    // Let the runtime know which UIViewController to restore after taking the user wherever the ad goes and add it to the view hierarchy.
    self.gbanner.rootViewController = gViewColtroller;
    [gView addSubview:self.gbanner];
    [self.gbanner loadRequest:self.request];
    
    self.show_ads_banner = TRUE;
    
    return self;
}

// Called before ad is shown, good time to show the add
- (void)adViewDidReceiveAd:(GADBannerView *)view
{
    NSLog(@"Admob load");
    self.gbanner.hidden = !self.show_ads_banner;
}

// An error occurred
- (void)adView:(GADBannerView *)view didFailToReceiveAdWithError:(GADRequestError *)error
{
    NSLog(@"Admob error: %@", error);
    self.gbanner.hidden = TRUE;
}

-(void)dealloc {
    NSLog(@"Freeing ads");
    if (self.gbanner) {        
        [self.gbanner removeFromSuperview];
        [self.gbanner release];
        self.gbanner.delegate = nil;
        self.gbanner = nil;
    }
    [super dealloc];
}

- (void)showAds:(int)ontop {
    self.show_ads_banner = TRUE;
    
    NSLog(@"Displaying banner object ontop:%d.", ontop);
    CGSize AdSize = kGADAdSizeBanner.size;
    CGRect frame = self.gbanner.frame;
    frame.origin.x = (gViewColtroller.view.bounds.size.width - AdSize.width) / 2 ;
    
    if (ontop)
        frame.origin.y = 0.0f; // gViewColtroller.view.bounds.size.height - AdSize.height;
    else
        frame.origin.y = 0.0f;
    self.gbanner.frame = frame;
}
@end


@interface adSwitchBanner : NSObject
@end
@implementation adSwitchBanner

-(id)init {
    if (!vbanner)
    {
        vbanner = [[myBanner alloc] init];
        [vbanner showAds:0];
    }
    return self;
}

-(void) show_ads {
    if (!vbanner)
        vbanner = [[myBanner alloc] init];
    [vbanner showAds:0];
}

-(void) hide_ads {
    if (vbanner)
    {
        [vbanner release];
        vbanner = nil;
    }
}

-(int) hidden_ad {
    if (vbanner)
        return 1;
    else
        return 0;
}
@end


@interface myInterstitial : NSObject <GADInterstitialDelegate>
@property (nonatomic, strong) GADInterstitial *interstitial;
@end

static myInterstitial *vinterstitial = nil;

@implementation myInterstitial

-(id)init{
    self.interstitial = [[GADInterstitial alloc] initWithAdUnitID:@"ca-app-pub-8564280870740386/5226855885"];
//    self.interstitial = [[GADInterstitial alloc] initWithAdUnitID:@"ca-app-pub-3940256099942544/1033173712"]; //google's test id's
    [self.interstitial setDelegate:self];
    GADRequest *request = [GADRequest request];
    [self.interstitial loadRequest:request];
    return self;
}

-(void)showInterstitialAds {
    UIWindow* win = [[UIApplication sharedApplication] keyWindow];
    UIViewController* vc = [win rootViewController];
    if (self.interstitial.isReady){
        [self.interstitial presentFromRootViewController:vc];
    }   else {
        NSLog(@"Ad wasn't ready");
    }
}
@end

@interface adSwitchInterstitial : NSObject
@end

@implementation adSwitchInterstitial
-(id)init {
    if (!vinterstitial){
        vinterstitial = [[myInterstitial alloc] init];
    }
    return self;
}

-(void) show_ads {
    if (!vinterstitial){
        vinterstitial = [[myInterstitial alloc] init];
    }
    [vinterstitial showInterstitialAds];
}

-(void) hide_ads {
    if (vinterstitial) {
        [vinterstitial release];
        vinterstitial = nil;
    }
}
@end


@interface myRewardVideo : NSObject <
