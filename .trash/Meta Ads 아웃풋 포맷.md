```
{
  "campaign": {
    "name": "Summer Sale Campaign",                     // ✅ 필수: 캠페인 이름
    "objective": "CONVERSIONS",                         // ✅ 필수: 광고 목표
    "status": "PAUSED",                                 // ✅ 필수: 상태
    "special_ad_categories": [],                        // ⚙️ 선택: 특수 카테고리 (예: EMPLOYMENT, HOUSING 등)
    "buying_type": "AUCTION"                            // ⚙️ 선택: 구매 유형 (기본값은 AUCTION)
  },
  "ad_set": {
    "name": "Retargeting Audience Set",                 // ✅ 필수
    "optimization_goal": "PURCHASE",                    // ✅ 필수
    "billing_event": "IMPRESSIONS",                     // ✅ 필수
    "bid_strategy": "LOWEST_COST_WITHOUT_CAP",          // ✅ 필수
    "daily_budget": 10000,                              // ✅ 필수 (또는 lifetime_budget)
    "lifetime_budget": null,                            // ⚙️ 선택: 전체 예산 (daily_budget 대신 사용 가능)
    "start_time": "2025-07-12T09:00:00+0900",           // ✅ 필수
    "end_time": "2025-07-18T23:59:59+0900",             // ✅ 필수

    "pacing_type": ["standard"],                        // ⚙️ 선택: 예산 소진 속도

    "targeting": {
      "age_min": 25,                                    // ✅ 필수
      "age_max": 45,                                    // ✅ 필수
      "genders": [1],                                   // ⚙️ 선택: 1(남), 2(여), 없으면 전체
      "geo_locations": {
        "countries": ["KR"],                            // ✅ 필수
        "regions": [{"key": "Seoul"}],                  // ⚙️ 선택
        "cities": [
          {
            "key": "2425605",                           // ⚙️ 선택: 지역 코드
            "radius": 10,
            "distance_unit": "mile"
          }
        ]
      },
      "interests": [
        {
          "id": "6003139266461",
          "name": "Cosmetics"
        }
      ],
      "custom_audiences": [
        {
          "id": "2384938493849384"
        }
      ],
      "excluded_custom_audiences": [
        {
          "id": "2384938493840000"
        }
      ],
      "publisher_platforms": ["facebook", "instagram"], // ⚙️ 선택: 게재 위치
      "device_platforms": ["mobile", "desktop"],        // ⚙️ 선택: 디바이스
      "user_device": ["iPhone", "Android_Smartphone"],  // ⚙️ 선택: 디바이스 모델
      "wireless_carrier": ["SK Telecom"]                // ⚙️ 선택: 통신사
    }
  },
  "creative": {
    "name": "Feed Creative v1",                         // ✅ 필수
    "title": "한여름 특가, 최대 50% 할인!",              // ✅ 필수
    "body": "지금 쇼핑하면 여름 한정 사은품 증정 🎁",   // ✅ 필수
    "link_url": "https://yourbrand.com/summer-sale",    // ✅ 필수
    "image_url": "https://yourbrand.com/assets/summer50.jpg", // ✅ 필수 (또는 video_id)
    "call_to_action": "SHOP_NOW",                       // ✅ 필수
    "link_caption": "지금 쇼핑하세요",                   // ⚙️ 선택
    "instagram_actor_id": "17841405822304914",          // ⚙️ 선택: 인스타 계정 연동 시
    "product_set_id": null                              // ⚙️ 선택: 카탈로그 광고용
  },
  "ad": {
    "name": "Feed Ad 001",                              // ✅ 필수
    "status": "PAUSED",                                 // ✅ 필수
    "tracking_specs": [                                 // ⚙️ 선택: Conversion 이벤트 추적
      {
        "action.type": ["offsite_conversion"],
        "fb_pixel": ["1234567890"]
      }
    ],
    "adlabels": [                                       // ⚙️ 선택: 광고 라벨
      {
        "name": "summer_promo"
      }
    ]
  }
}
```