window.DEMO = {
 "mill": "Rayalaseema Steel Rolling",
 "see": 1.9,
 "states": {
  "after": {
   "curve": [
    {
     "default": 9574.752900000001,
     "year": 2026,
     "yours": 4198.7529
    },
    {
     "default": 20826.505800000003,
     "year": 2027,
     "yours": 8397.5058
    },
    {
     "default": 45007.01160000001,
     "year": 2028,
     "yours": 16795.0116
    },
    {
     "default": 101265.77610000003,
     "year": 2029,
     "yours": 37788.776099999995
    },
    {
     "default": 218284.00626000002,
     "year": 2030,
     "yours": 81455.80626
    },
    {
     "default": 274542.77076000004,
     "year": 2031,
     "yours": 102449.57076
    },
    {
     "default": 330801.5352600001,
     "year": 2032,
     "yours": 123443.33525999999
    },
    {
     "default": 387060.29976,
     "year": 2033,
     "yours": 144437.09975999998
    },
    {
     "default": 450070.11600000004,
     "year": 2034,
     "yours": 167950.11599999998
    }
   ],
   "years": {
    "2026": {
     "audit": {
      "checks": [],
      "default_note": "Steel default used: 4.3 tCO2/t before the mark-up. Secondary source. Check it against the current EU table.",
      "draft": "Draft. Not verified. Indirect emissions are not counted for iron and steel goods.",
      "method": [
       "Installation: Sri Venkateswara Fasteners (your plant)",
       "Goods: screws, bolts and nuts (CN 7318)",
       "Route: wire rod, cold heading, heat treatment, plating",
       "Method: calculation-based. Activity data x standard emission factor. Direct emissions only.",
       "diesel: purchase invoices only.",
       "lpg: used = opening stock + purchases - closing stock, logged monthly (2026-04 to 2026-05). Measured by: Weighbridge WB-2, calibrated 2026-01.",
       "Output: dispatch records.",
       "Precursor steel from Kaveri Integrated Steel: verified actual value.",
       "Precursor steel from Rayalaseema Steel Rolling: verified actual value."
      ],
      "plan": {
       "gaps": [
        "diesel: only purchase invoices. Purchases are not usage. Start a monthly stock log.",
        "lpg: 2 of 12 months logged.",
        "Output: no monthly production log. Log tonnes made each month."
       ],
       "lines": [
        "Installation: Sri Venkateswara Fasteners (your plant)",
        "Goods: screws, bolts and nuts (CN 7318)",
        "Route: wire rod, cold heading, heat treatment, plating",
        "Method: calculation-based. Activity data x standard emission factor. Direct emissions only.",
        "diesel: purchase invoices only.",
        "lpg: used = opening stock + purchases - closing stock, logged monthly (2026-04 to 2026-05). Measured by: Weighbridge WB-2, calibrated 2026-01.",
        "Output: dispatch records.",
        "Precursor steel from Kaveri Integrated Steel: verified actual value.",
        "Precursor steel from Rayalaseema Steel Rolling: verified actual value."
       ]
      },
      "rows": [
       {
        "basis": "actual",
        "item": "fuel diesel 12000.0 litre",
        "kind": "fuel",
        "sources": [
         {
          "file": "fuel_3.txt",
          "quote": "Quantity: 12000 litre",
          "role": "quantity"
         }
        ],
        "tco2": 32.115
       },
       {
        "basis": "actual",
        "item": "fuel lpg 28 t",
        "kind": "fuel",
        "sources": [
         {
          "file": "monthly log 2026-04",
          "quote": "opening 6 + bought 30 - closing 8",
          "role": "quantity"
         }
        ],
        "tco2": 83.58
       },
       {
        "basis": "actual",
        "item": "fuel lpg 24 t",
        "kind": "fuel",
        "sources": [
         {
          "file": "monthly log 2026-05",
          "quote": "opening 8 + bought 26 - closing 10",
          "role": "quantity"
         }
        ],
        "tco2": 71.64
       },
       {
        "basis": "actual 1.9 tCO2/t Verification report RSR-2026-031 (demo)",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0412 180.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_1.txt",
          "quote": "Steel (t): 180",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 342.0
       },
       {
        "basis": "actual 1.9 tCO2/t Verification report RSR-2026-031 (demo)",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0419 170.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_2.txt",
          "quote": "Steel (t): 170",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 323.0
       },
       {
        "basis": "actual 1.9 tCO2/t Verification report RSR-2026-031 (demo)",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0533 160.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_3.txt",
          "quote": "Steel (t): 160",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 304.0
       },
       {
        "basis": "actual 1.9 tCO2/t Verification report RSR-2026-031 (demo)",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0610 150.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_4.txt",
          "quote": "Steel (t): 150",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 285.0
       },
       {
        "basis": "actual 2.1 tCO2/t Verification report KIS-2026-114 (demo)",
        "item": "steel Kaveri Integrated Steel heat KIS-H88213 200.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_5.txt",
          "quote": "Steel (t): 200",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 420.0
       },
       {
        "basis": "actual 2.1 tCO2/t Verification report KIS-2026-114 (demo)",
        "item": "steel Kaveri Integrated Steel heat KIS-H88457 180.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "steel_invoice_1.txt",
          "quote": "Steel (t): 180",
          "role": "tonnes"
         },
         {
          "file": "mtc_6.txt",
          "quote": "Quantity: 46 coils",
          "role": "mill"
         }
        ],
        "tco2": 378.0
       },
       {
        "basis": "",
        "item": "output 1000.0 t",
        "kind": "output",
        "sources": [
         {
          "file": "production.txt",
          "quote": "Output (t): 1000",
          "role": "output"
         }
        ],
        "tco2": null
       }
      ],
      "summary": {
       "name": "Sri Venkateswara Fasteners (your plant)",
       "output_t": 1000.0,
       "see_direct": 0.18733488,
       "see_precursor": 2.052,
       "see_total": 2.23933488,
       "verified_share": 1.0,
       "year": 2026
      }
     },
     "plants": [
      {
       "id": "A",
       "name": "Sri Venkateswara Fasteners (your plant)",
       "see_direct": 0.18733488,
       "see_precursor": 2.052,
       "see_total": 2.23933488,
       "verified_share": 1.0
      },
      {
       "id": "B",
       "name": "Chennai Bolt Works",
       "see_direct": 0.13776923076923075,
       "see_precursor": 2.0,
       "see_total": 2.137769230769231,
       "verified_share": 1.0
      },
      {
       "id": "C",
       "name": "Hyderabad Wire & Fasteners",
       "see_direct": 0.15546875,
       "see_precursor": 1.9791666666666667,
       "see_total": 2.134635416666667,
       "verified_share": 1.0
      },
      {
       "id": "D",
       "name": "Nellore Screws",
       "see_direct": 0.1053529411764706,
       "see_precursor": 3.2044117647058825,
       "see_total": 3.309764705882353,
       "verified_share": 0.5714285714285714
      }
     ]
    },
    "2027": {
     "audit": {
      "checks": [],
      "default_note": "Steel default used: 4.3 tCO2/t before the mark-up. Secondary source. Check it against the current EU table.",
      "draft": "Draft. Not verified. Indirect emissions are not counted for iron and steel goods.",
      "method": [
       "Installation: Sri Venkateswara Fasteners (your plant)",
       "Goods: screws, bolts and nuts (CN 7318)",
       "Route: wire rod, cold heading, heat treatment, plating",
       "Method: calculation-based. Activity data x standard emission factor. Direct emissions only.",
       "diesel: purchase invoices only.",
       "lpg: used = opening stock + purchases - closing stock, logged monthly (2026-04 to 2026-05). Measured by: Weighbridge WB-2, calibrated 2026-01.",
       "Output: dispatch records.",
       "Precursor steel from Kaveri Integrated Steel: verified actual value.",
       "Precursor steel from Rayalaseema Steel Rolling: verified actual value."
      ],
      "plan": {
       "gaps": [
        "diesel: only purchase invoices. Purchases are not usage. Start a monthly stock log.",
        "lpg: 2 of 12 months logged.",
        "Output: no monthly production log. Log tonnes made each month."
       ],
       "lines": [
        "Installation: Sri Venkateswara Fasteners (your plant)",
        "Goods: screws, bolts and nuts (CN 7318)",
        "Route: wire rod, cold heading, heat treatment, plating",
        "Method: calculation-based. Activity data x standard emission factor. Direct emissions only.",
        "diesel: purchase invoices only.",
        "lpg: used = opening stock + purchases - closing stock, logged monthly (2026-04 to 2026-05). Measured by: Weighbridge WB-2, calibrated 2026-01.",
        "Output: dispatch records.",
        "Precursor steel from Kaveri Integrated Steel: verified actual value.",
        "Precursor steel from Rayalaseema Steel Rolling: verified actual value."
       ]
      },
      "rows": [
       {
        "basis": "actual",
        "item": "fuel diesel 12000.0 litre",
        "kind": "fuel",
        "sources": [
         {
          "file": "fuel_3.txt",
          "quote": "Quantity: 12000 litre",
          "role": "quantity"
         }
        ],
        "tco2": 32.115
       },
       {
        "basis": "actual",
        "item": "fuel lpg 28 t",
        "kind": "fuel",
        "sources": [
         {
          "file": "monthly log 2026-04",
          "quote": "opening 6 + bought 30 - closing 8",
          "role": "quantity"
         }
        ],
        "tco2": 83.58
       },
       {
        "basis": "actual",
        "item": "fuel lpg 24 t",
        "kind": "fuel",
        "sources": [
         {
          "file": "monthly log 2026-05",
          "quote": "opening 8 + bought 26 - closing 10",
          "role": "quantity"
         }
        ],
        "tco2": 71.64
       },
       {
        "basis": "actual 1.9 tCO2/t Verification report RSR-2026-031 (demo)",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0412 180.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_1.txt",
          "quote": "Steel (t): 180",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 342.0
       },
       {
        "basis": "actual 1.9 tCO2/t Verification report RSR-2026-031 (demo)",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0419 170.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_2.txt",
          "quote": "Steel (t): 170",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 323.0
       },
       {
        "basis": "actual 1.9 tCO2/t Verification report RSR-2026-031 (demo)",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0533 160.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_3.txt",
          "quote": "Steel (t): 160",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 304.0
       },
       {
        "basis": "actual 1.9 tCO2/t Verification report RSR-2026-031 (demo)",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0610 150.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_4.txt",
          "quote": "Steel (t): 150",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 285.0
       },
       {
        "basis": "actual 2.1 tCO2/t Verification report KIS-2026-114 (demo)",
        "item": "steel Kaveri Integrated Steel heat KIS-H88213 200.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_5.txt",
          "quote": "Steel (t): 200",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 420.0
       },
       {
        "basis": "actual 2.1 tCO2/t Verification report KIS-2026-114 (demo)",
        "item": "steel Kaveri Integrated Steel heat KIS-H88457 180.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "steel_invoice_1.txt",
          "quote": "Steel (t): 180",
          "role": "tonnes"
         },
         {
          "file": "mtc_6.txt",
          "quote": "Quantity: 46 coils",
          "role": "mill"
         }
        ],
        "tco2": 378.0
       },
       {
        "basis": "",
        "item": "output 1000.0 t",
        "kind": "output",
        "sources": [
         {
          "file": "production.txt",
          "quote": "Output (t): 1000",
          "role": "output"
         }
        ],
        "tco2": null
       }
      ],
      "summary": {
       "name": "Sri Venkateswara Fasteners (your plant)",
       "output_t": 1000.0,
       "see_direct": 0.18733488,
       "see_precursor": 2.052,
       "see_total": 2.23933488,
       "verified_share": 1.0,
       "year": 2027
      }
     },
     "plants": [
      {
       "id": "A",
       "name": "Sri Venkateswara Fasteners (your plant)",
       "see_direct": 0.18733488,
       "see_precursor": 2.052,
       "see_total": 2.23933488,
       "verified_share": 1.0
      },
      {
       "id": "B",
       "name": "Chennai Bolt Works",
       "see_direct": 0.13776923076923075,
       "see_precursor": 2.0,
       "see_total": 2.137769230769231,
       "verified_share": 1.0
      },
      {
       "id": "C",
       "name": "Hyderabad Wire & Fasteners",
       "see_direct": 0.15546875,
       "see_precursor": 1.9791666666666667,
       "see_total": 2.134635416666667,
       "verified_share": 1.0
      },
      {
       "id": "D",
       "name": "Nellore Screws",
       "see_direct": 0.1053529411764706,
       "see_precursor": 3.3941176470588235,
       "see_total": 3.499470588235294,
       "verified_share": 0.5714285714285714
      }
     ]
    },
    "2028": {
     "audit": {
      "checks": [],
      "default_note": "Steel default used: 4.3 tCO2/t before the mark-up. Secondary source. Check it against the current EU table.",
      "draft": "Draft. Not verified. Indirect emissions are not counted for iron and steel goods.",
      "method": [
       "Installation: Sri Venkateswara Fasteners (your plant)",
       "Goods: screws, bolts and nuts (CN 7318)",
       "Route: wire rod, cold heading, heat treatment, plating",
       "Method: calculation-based. Activity data x standard emission factor. Direct emissions only.",
       "diesel: purchase invoices only.",
       "lpg: used = opening stock + purchases - closing stock, logged monthly (2026-04 to 2026-05). Measured by: Weighbridge WB-2, calibrated 2026-01.",
       "Output: dispatch records.",
       "Precursor steel from Kaveri Integrated Steel: verified actual value.",
       "Precursor steel from Rayalaseema Steel Rolling: verified actual value."
      ],
      "plan": {
       "gaps": [
        "diesel: only purchase invoices. Purchases are not usage. Start a monthly stock log.",
        "lpg: 2 of 12 months logged.",
        "Output: no monthly production log. Log tonnes made each month."
       ],
       "lines": [
        "Installation: Sri Venkateswara Fasteners (your plant)",
        "Goods: screws, bolts and nuts (CN 7318)",
        "Route: wire rod, cold heading, heat treatment, plating",
        "Method: calculation-based. Activity data x standard emission factor. Direct emissions only.",
        "diesel: purchase invoices only.",
        "lpg: used = opening stock + purchases - closing stock, logged monthly (2026-04 to 2026-05). Measured by: Weighbridge WB-2, calibrated 2026-01.",
        "Output: dispatch records.",
        "Precursor steel from Kaveri Integrated Steel: verified actual value.",
        "Precursor steel from Rayalaseema Steel Rolling: verified actual value."
       ]
      },
      "rows": [
       {
        "basis": "actual",
        "item": "fuel diesel 12000.0 litre",
        "kind": "fuel",
        "sources": [
         {
          "file": "fuel_3.txt",
          "quote": "Quantity: 12000 litre",
          "role": "quantity"
         }
        ],
        "tco2": 32.115
       },
       {
        "basis": "actual",
        "item": "fuel lpg 28 t",
        "kind": "fuel",
        "sources": [
         {
          "file": "monthly log 2026-04",
          "quote": "opening 6 + bought 30 - closing 8",
          "role": "quantity"
         }
        ],
        "tco2": 83.58
       },
       {
        "basis": "actual",
        "item": "fuel lpg 24 t",
        "kind": "fuel",
        "sources": [
         {
          "file": "monthly log 2026-05",
          "quote": "opening 8 + bought 26 - closing 10",
          "role": "quantity"
         }
        ],
        "tco2": 71.64
       },
       {
        "basis": "actual 1.9 tCO2/t Verification report RSR-2026-031 (demo)",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0412 180.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_1.txt",
          "quote": "Steel (t): 180",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 342.0
       },
       {
        "basis": "actual 1.9 tCO2/t Verification report RSR-2026-031 (demo)",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0419 170.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_2.txt",
          "quote": "Steel (t): 170",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 323.0
       },
       {
        "basis": "actual 1.9 tCO2/t Verification report RSR-2026-031 (demo)",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0533 160.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_3.txt",
          "quote": "Steel (t): 160",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 304.0
       },
       {
        "basis": "actual 1.9 tCO2/t Verification report RSR-2026-031 (demo)",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0610 150.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_4.txt",
          "quote": "Steel (t): 150",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 285.0
       },
       {
        "basis": "actual 2.1 tCO2/t Verification report KIS-2026-114 (demo)",
        "item": "steel Kaveri Integrated Steel heat KIS-H88213 200.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_5.txt",
          "quote": "Steel (t): 200",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 420.0
       },
       {
        "basis": "actual 2.1 tCO2/t Verification report KIS-2026-114 (demo)",
        "item": "steel Kaveri Integrated Steel heat KIS-H88457 180.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "steel_invoice_1.txt",
          "quote": "Steel (t): 180",
          "role": "tonnes"
         },
         {
          "file": "mtc_6.txt",
          "quote": "Quantity: 46 coils",
          "role": "mill"
         }
        ],
        "tco2": 378.0
       },
       {
        "basis": "",
        "item": "output 1000.0 t",
        "kind": "output",
        "sources": [
         {
          "file": "production.txt",
          "quote": "Output (t): 1000",
          "role": "output"
         }
        ],
        "tco2": null
       }
      ],
      "summary": {
       "name": "Sri Venkateswara Fasteners (your plant)",
       "output_t": 1000.0,
       "see_direct": 0.18733488,
       "see_precursor": 2.052,
       "see_total": 2.23933488,
       "verified_share": 1.0,
       "year": 2028
      }
     },
     "plants": [
      {
       "id": "A",
       "name": "Sri Venkateswara Fasteners (your plant)",
       "see_direct": 0.18733488,
       "see_precursor": 2.052,
       "see_total": 2.23933488,
       "verified_share": 1.0
      },
      {
       "id": "B",
       "name": "Chennai Bolt Works",
       "see_direct": 0.13776923076923075,
       "see_precursor": 2.0,
       "see_total": 2.137769230769231,
       "verified_share": 1.0
      },
      {
       "id": "C",
       "name": "Hyderabad Wire & Fasteners",
       "see_direct": 0.15546875,
       "see_precursor": 1.9791666666666667,
       "see_total": 2.134635416666667,
       "verified_share": 1.0
      },
      {
       "id": "D",
       "name": "Nellore Screws",
       "see_direct": 0.1053529411764706,
       "see_precursor": 3.583823529411765,
       "see_total": 3.6891764705882353,
       "verified_share": 0.5714285714285714
      }
     ]
    },
    "2029": {
     "audit": {
      "checks": [],
      "default_note": "Steel default used: 4.3 tCO2/t before the mark-up. Secondary source. Check it against the current EU table.",
      "draft": "Draft. Not verified. Indirect emissions are not counted for iron and steel goods.",
      "method": [
       "Installation: Sri Venkateswara Fasteners (your plant)",
       "Goods: screws, bolts and nuts (CN 7318)",
       "Route: wire rod, cold heading, heat treatment, plating",
       "Method: calculation-based. Activity data x standard emission factor. Direct emissions only.",
       "diesel: purchase invoices only.",
       "lpg: used = opening stock + purchases - closing stock, logged monthly (2026-04 to 2026-05). Measured by: Weighbridge WB-2, calibrated 2026-01.",
       "Output: dispatch records.",
       "Precursor steel from Kaveri Integrated Steel: verified actual value.",
       "Precursor steel from Rayalaseema Steel Rolling: verified actual value."
      ],
      "plan": {
       "gaps": [
        "diesel: only purchase invoices. Purchases are not usage. Start a monthly stock log.",
        "lpg: 2 of 12 months logged.",
        "Output: no monthly production log. Log tonnes made each month."
       ],
       "lines": [
        "Installation: Sri Venkateswara Fasteners (your plant)",
        "Goods: screws, bolts and nuts (CN 7318)",
        "Route: wire rod, cold heading, heat treatment, plating",
        "Method: calculation-based. Activity data x standard emission factor. Direct emissions only.",
        "diesel: purchase invoices only.",
        "lpg: used = opening stock + purchases - closing stock, logged monthly (2026-04 to 2026-05). Measured by: Weighbridge WB-2, calibrated 2026-01.",
        "Output: dispatch records.",
        "Precursor steel from Kaveri Integrated Steel: verified actual value.",
        "Precursor steel from Rayalaseema Steel Rolling: verified actual value."
       ]
      },
      "rows": [
       {
        "basis": "actual",
        "item": "fuel diesel 12000.0 litre",
        "kind": "fuel",
        "sources": [
         {
          "file": "fuel_3.txt",
          "quote": "Quantity: 12000 litre",
          "role": "quantity"
         }
        ],
        "tco2": 32.115
       },
       {
        "basis": "actual",
        "item": "fuel lpg 28 t",
        "kind": "fuel",
        "sources": [
         {
          "file": "monthly log 2026-04",
          "quote": "opening 6 + bought 30 - closing 8",
          "role": "quantity"
         }
        ],
        "tco2": 83.58
       },
       {
        "basis": "actual",
        "item": "fuel lpg 24 t",
        "kind": "fuel",
        "sources": [
         {
          "file": "monthly log 2026-05",
          "quote": "opening 8 + bought 26 - closing 10",
          "role": "quantity"
         }
        ],
        "tco2": 71.64
       },
       {
        "basis": "actual 1.9 tCO2/t Verification report RSR-2026-031 (demo)",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0412 180.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_1.txt",
          "quote": "Steel (t): 180",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 342.0
       },
       {
        "basis": "actual 1.9 tCO2/t Verification report RSR-2026-031 (demo)",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0419 170.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_2.txt",
          "quote": "Steel (t): 170",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 323.0
       },
       {
        "basis": "actual 1.9 tCO2/t Verification report RSR-2026-031 (demo)",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0533 160.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_3.txt",
          "quote": "Steel (t): 160",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 304.0
       },
       {
        "basis": "actual 1.9 tCO2/t Verification report RSR-2026-031 (demo)",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0610 150.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_4.txt",
          "quote": "Steel (t): 150",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 285.0
       },
       {
        "basis": "actual 2.1 tCO2/t Verification report KIS-2026-114 (demo)",
        "item": "steel Kaveri Integrated Steel heat KIS-H88213 200.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_5.txt",
          "quote": "Steel (t): 200",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 420.0
       },
       {
        "basis": "actual 2.1 tCO2/t Verification report KIS-2026-114 (demo)",
        "item": "steel Kaveri Integrated Steel heat KIS-H88457 180.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "steel_invoice_1.txt",
          "quote": "Steel (t): 180",
          "role": "tonnes"
         },
         {
          "file": "mtc_6.txt",
          "quote": "Quantity: 46 coils",
          "role": "mill"
         }
        ],
        "tco2": 378.0
       },
       {
        "basis": "",
        "item": "output 1000.0 t",
        "kind": "output",
        "sources": [
         {
          "file": "production.txt",
          "quote": "Output (t): 1000",
          "role": "output"
         }
        ],
        "tco2": null
       }
      ],
      "summary": {
       "name": "Sri Venkateswara Fasteners (your plant)",
       "output_t": 1000.0,
       "see_direct": 0.18733488,
       "see_precursor": 2.052,
       "see_total": 2.23933488,
       "verified_share": 1.0,
       "year": 2029
      }
     },
     "plants": [
      {
       "id": "A",
       "name": "Sri Venkateswara Fasteners (your plant)",
       "see_direct": 0.18733488,
       "see_precursor": 2.052,
       "see_total": 2.23933488,
       "verified_share": 1.0
      },
      {
       "id": "B",
       "name": "Chennai Bolt Works",
       "see_direct": 0.13776923076923075,
       "see_precursor": 2.0,
       "see_total": 2.137769230769231,
       "verified_share": 1.0
      },
      {
       "id": "C",
       "name": "Hyderabad Wire & Fasteners",
       "see_direct": 0.15546875,
       "see_precursor": 1.9791666666666667,
       "see_total": 2.134635416666667,
       "verified_share": 1.0
      },
      {
       "id": "D",
       "name": "Nellore Screws",
       "see_direct": 0.1053529411764706,
       "see_precursor": 3.583823529411765,
       "see_total": 3.6891764705882353,
       "verified_share": 0.5714285714285714
      }
     ]
    },
    "2030": {
     "audit": {
      "checks": [],
      "default_note": "Steel default used: 4.3 tCO2/t before the mark-up. Secondary source. Check it against the current EU table.",
      "draft": "Draft. Not verified. Indirect emissions are not counted for iron and steel goods.",
      "method": [
       "Installation: Sri Venkateswara Fasteners (your plant)",
       "Goods: screws, bolts and nuts (CN 7318)",
       "Route: wire rod, cold heading, heat treatment, plating",
       "Method: calculation-based. Activity data x standard emission factor. Direct emissions only.",
       "diesel: purchase invoices only.",
       "lpg: used = opening stock + purchases - closing stock, logged monthly (2026-04 to 2026-05). Measured by: Weighbridge WB-2, calibrated 2026-01.",
       "Output: dispatch records.",
       "Precursor steel from Kaveri Integrated Steel: verified actual value.",
       "Precursor steel from Rayalaseema Steel Rolling: verified actual value."
      ],
      "plan": {
       "gaps": [
        "diesel: only purchase invoices. Purchases are not usage. Start a monthly stock log.",
        "lpg: 2 of 12 months logged.",
        "Output: no monthly production log. Log tonnes made each month."
       ],
       "lines": [
        "Installation: Sri Venkateswara Fasteners (your plant)",
        "Goods: screws, bolts and nuts (CN 7318)",
        "Route: wire rod, cold heading, heat treatment, plating",
        "Method: calculation-based. Activity data x standard emission factor. Direct emissions only.",
        "diesel: purchase invoices only.",
        "lpg: used = opening stock + purchases - closing stock, logged monthly (2026-04 to 2026-05). Measured by: Weighbridge WB-2, calibrated 2026-01.",
        "Output: dispatch records.",
        "Precursor steel from Kaveri Integrated Steel: verified actual value.",
        "Precursor steel from Rayalaseema Steel Rolling: verified actual value."
       ]
      },
      "rows": [
       {
        "basis": "actual",
        "item": "fuel diesel 12000.0 litre",
        "kind": "fuel",
        "sources": [
         {
          "file": "fuel_3.txt",
          "quote": "Quantity: 12000 litre",
          "role": "quantity"
         }
        ],
        "tco2": 32.115
       },
       {
        "basis": "actual",
        "item": "fuel lpg 28 t",
        "kind": "fuel",
        "sources": [
         {
          "file": "monthly log 2026-04",
          "quote": "opening 6 + bought 30 - closing 8",
          "role": "quantity"
         }
        ],
        "tco2": 83.58
       },
       {
        "basis": "actual",
        "item": "fuel lpg 24 t",
        "kind": "fuel",
        "sources": [
         {
          "file": "monthly log 2026-05",
          "quote": "opening 8 + bought 26 - closing 10",
          "role": "quantity"
         }
        ],
        "tco2": 71.64
       },
       {
        "basis": "actual 1.9 tCO2/t Verification report RSR-2026-031 (demo)",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0412 180.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_1.txt",
          "quote": "Steel (t): 180",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 342.0
       },
       {
        "basis": "actual 1.9 tCO2/t Verification report RSR-2026-031 (demo)",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0419 170.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_2.txt",
          "quote": "Steel (t): 170",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 323.0
       },
       {
        "basis": "actual 1.9 tCO2/t Verification report RSR-2026-031 (demo)",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0533 160.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_3.txt",
          "quote": "Steel (t): 160",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 304.0
       },
       {
        "basis": "actual 1.9 tCO2/t Verification report RSR-2026-031 (demo)",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0610 150.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_4.txt",
          "quote": "Steel (t): 150",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 285.0
       },
       {
        "basis": "actual 2.1 tCO2/t Verification report KIS-2026-114 (demo)",
        "item": "steel Kaveri Integrated Steel heat KIS-H88213 200.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_5.txt",
          "quote": "Steel (t): 200",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 420.0
       },
       {
        "basis": "actual 2.1 tCO2/t Verification report KIS-2026-114 (demo)",
        "item": "steel Kaveri Integrated Steel heat KIS-H88457 180.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "steel_invoice_1.txt",
          "quote": "Steel (t): 180",
          "role": "tonnes"
         },
         {
          "file": "mtc_6.txt",
          "quote": "Quantity: 46 coils",
          "role": "mill"
         }
        ],
        "tco2": 378.0
       },
       {
        "basis": "",
        "item": "output 1000.0 t",
        "kind": "output",
        "sources": [
         {
          "file": "production.txt",
          "quote": "Output (t): 1000",
          "role": "output"
         }
        ],
        "tco2": null
       }
      ],
      "summary": {
       "name": "Sri Venkateswara Fasteners (your plant)",
       "output_t": 1000.0,
       "see_direct": 0.18733488,
       "see_precursor": 2.052,
       "see_total": 2.23933488,
       "verified_share": 1.0,
       "year": 2030
      }
     },
     "plants": [
      {
       "id": "A",
       "name": "Sri Venkateswara Fasteners (your plant)",
       "see_direct": 0.18733488,
       "see_precursor": 2.052,
       "see_total": 2.23933488,
       "verified_share": 1.0
      },
      {
       "id": "B",
       "name": "Chennai Bolt Works",
       "see_direct": 0.13776923076923075,
       "see_precursor": 2.0,
       "see_total": 2.137769230769231,
       "verified_share": 1.0
      },
      {
       "id": "C",
       "name": "Hyderabad Wire & Fasteners",
       "see_direct": 0.15546875,
       "see_precursor": 1.9791666666666667,
       "see_total": 2.134635416666667,
       "verified_share": 1.0
      },
      {
       "id": "D",
       "name": "Nellore Screws",
       "see_direct": 0.1053529411764706,
       "see_precursor": 3.583823529411765,
       "see_total": 3.6891764705882353,
       "verified_share": 0.5714285714285714
      }
     ]
    },
    "2031": {
     "audit": {
      "checks": [],
      "default_note": "Steel default used: 4.3 tCO2/t before the mark-up. Secondary source. Check it against the current EU table.",
      "draft": "Draft. Not verified. Indirect emissions are not counted for iron and steel goods.",
      "method": [
       "Installation: Sri Venkateswara Fasteners (your plant)",
       "Goods: screws, bolts and nuts (CN 7318)",
       "Route: wire rod, cold heading, heat treatment, plating",
       "Method: calculation-based. Activity data x standard emission factor. Direct emissions only.",
       "diesel: purchase invoices only.",
       "lpg: used = opening stock + purchases - closing stock, logged monthly (2026-04 to 2026-05). Measured by: Weighbridge WB-2, calibrated 2026-01.",
       "Output: dispatch records.",
       "Precursor steel from Kaveri Integrated Steel: verified actual value.",
       "Precursor steel from Rayalaseema Steel Rolling: verified actual value."
      ],
      "plan": {
       "gaps": [
        "diesel: only purchase invoices. Purchases are not usage. Start a monthly stock log.",
        "lpg: 2 of 12 months logged.",
        "Output: no monthly production log. Log tonnes made each month."
       ],
       "lines": [
        "Installation: Sri Venkateswara Fasteners (your plant)",
        "Goods: screws, bolts and nuts (CN 7318)",
        "Route: wire rod, cold heading, heat treatment, plating",
        "Method: calculation-based. Activity data x standard emission factor. Direct emissions only.",
        "diesel: purchase invoices only.",
        "lpg: used = opening stock + purchases - closing stock, logged monthly (2026-04 to 2026-05). Measured by: Weighbridge WB-2, calibrated 2026-01.",
        "Output: dispatch records.",
        "Precursor steel from Kaveri Integrated Steel: verified actual value.",
        "Precursor steel from Rayalaseema Steel Rolling: verified actual value."
       ]
      },
      "rows": [
       {
        "basis": "actual",
        "item": "fuel diesel 12000.0 litre",
        "kind": "fuel",
        "sources": [
         {
          "file": "fuel_3.txt",
          "quote": "Quantity: 12000 litre",
          "role": "quantity"
         }
        ],
        "tco2": 32.115
       },
       {
        "basis": "actual",
        "item": "fuel lpg 28 t",
        "kind": "fuel",
        "sources": [
         {
          "file": "monthly log 2026-04",
          "quote": "opening 6 + bought 30 - closing 8",
          "role": "quantity"
         }
        ],
        "tco2": 83.58
       },
       {
        "basis": "actual",
        "item": "fuel lpg 24 t",
        "kind": "fuel",
        "sources": [
         {
          "file": "monthly log 2026-05",
          "quote": "opening 8 + bought 26 - closing 10",
          "role": "quantity"
         }
        ],
        "tco2": 71.64
       },
       {
        "basis": "actual 1.9 tCO2/t Verification report RSR-2026-031 (demo)",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0412 180.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_1.txt",
          "quote": "Steel (t): 180",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 342.0
       },
       {
        "basis": "actual 1.9 tCO2/t Verification report RSR-2026-031 (demo)",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0419 170.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_2.txt",
          "quote": "Steel (t): 170",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 323.0
       },
       {
        "basis": "actual 1.9 tCO2/t Verification report RSR-2026-031 (demo)",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0533 160.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_3.txt",
          "quote": "Steel (t): 160",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 304.0
       },
       {
        "basis": "actual 1.9 tCO2/t Verification report RSR-2026-031 (demo)",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0610 150.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_4.txt",
          "quote": "Steel (t): 150",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 285.0
       },
       {
        "basis": "actual 2.1 tCO2/t Verification report KIS-2026-114 (demo)",
        "item": "steel Kaveri Integrated Steel heat KIS-H88213 200.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_5.txt",
          "quote": "Steel (t): 200",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 420.0
       },
       {
        "basis": "actual 2.1 tCO2/t Verification report KIS-2026-114 (demo)",
        "item": "steel Kaveri Integrated Steel heat KIS-H88457 180.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "steel_invoice_1.txt",
          "quote": "Steel (t): 180",
          "role": "tonnes"
         },
         {
          "file": "mtc_6.txt",
          "quote": "Quantity: 46 coils",
          "role": "mill"
         }
        ],
        "tco2": 378.0
       },
       {
        "basis": "",
        "item": "output 1000.0 t",
        "kind": "output",
        "sources": [
         {
          "file": "production.txt",
          "quote": "Output (t): 1000",
          "role": "output"
         }
        ],
        "tco2": null
       }
      ],
      "summary": {
       "name": "Sri Venkateswara Fasteners (your plant)",
       "output_t": 1000.0,
       "see_direct": 0.18733488,
       "see_precursor": 2.052,
       "see_total": 2.23933488,
       "verified_share": 1.0,
       "year": 2031
      }
     },
     "plants": [
      {
       "id": "A",
       "name": "Sri Venkateswara Fasteners (your plant)",
       "see_direct": 0.18733488,
       "see_precursor": 2.052,
       "see_total": 2.23933488,
       "verified_share": 1.0
      },
      {
       "id": "B",
       "name": "Chennai Bolt Works",
       "see_direct": 0.13776923076923075,
       "see_precursor": 2.0,
       "see_total": 2.137769230769231,
       "verified_share": 1.0
      },
      {
       "id": "C",
       "name": "Hyderabad Wire & Fasteners",
       "see_direct": 0.15546875,
       "see_precursor": 1.9791666666666667,
       "see_total": 2.134635416666667,
       "verified_share": 1.0
      },
      {
       "id": "D",
       "name": "Nellore Screws",
       "see_direct": 0.1053529411764706,
       "see_precursor": 3.583823529411765,
       "see_total": 3.6891764705882353,
       "verified_share": 0.5714285714285714
      }
     ]
    },
    "2032": {
     "audit": {
      "checks": [],
      "default_note": "Steel default used: 4.3 tCO2/t before the mark-up. Secondary source. Check it against the current EU table.",
      "draft": "Draft. Not verified. Indirect emissions are not counted for iron and steel goods.",
      "method": [
       "Installation: Sri Venkateswara Fasteners (your plant)",
       "Goods: screws, bolts and nuts (CN 7318)",
       "Route: wire rod, cold heading, heat treatment, plating",
       "Method: calculation-based. Activity data x standard emission factor. Direct emissions only.",
       "diesel: purchase invoices only.",
       "lpg: used = opening stock + purchases - closing stock, logged monthly (2026-04 to 2026-05). Measured by: Weighbridge WB-2, calibrated 2026-01.",
       "Output: dispatch records.",
       "Precursor steel from Kaveri Integrated Steel: verified actual value.",
       "Precursor steel from Rayalaseema Steel Rolling: verified actual value."
      ],
      "plan": {
       "gaps": [
        "diesel: only purchase invoices. Purchases are not usage. Start a monthly stock log.",
        "lpg: 2 of 12 months logged.",
        "Output: no monthly production log. Log tonnes made each month."
       ],
       "lines": [
        "Installation: Sri Venkateswara Fasteners (your plant)",
        "Goods: screws, bolts and nuts (CN 7318)",
        "Route: wire rod, cold heading, heat treatment, plating",
        "Method: calculation-based. Activity data x standard emission factor. Direct emissions only.",
        "diesel: purchase invoices only.",
        "lpg: used = opening stock + purchases - closing stock, logged monthly (2026-04 to 2026-05). Measured by: Weighbridge WB-2, calibrated 2026-01.",
        "Output: dispatch records.",
        "Precursor steel from Kaveri Integrated Steel: verified actual value.",
        "Precursor steel from Rayalaseema Steel Rolling: verified actual value."
       ]
      },
      "rows": [
       {
        "basis": "actual",
        "item": "fuel diesel 12000.0 litre",
        "kind": "fuel",
        "sources": [
         {
          "file": "fuel_3.txt",
          "quote": "Quantity: 12000 litre",
          "role": "quantity"
         }
        ],
        "tco2": 32.115
       },
       {
        "basis": "actual",
        "item": "fuel lpg 28 t",
        "kind": "fuel",
        "sources": [
         {
          "file": "monthly log 2026-04",
          "quote": "opening 6 + bought 30 - closing 8",
          "role": "quantity"
         }
        ],
        "tco2": 83.58
       },
       {
        "basis": "actual",
        "item": "fuel lpg 24 t",
        "kind": "fuel",
        "sources": [
         {
          "file": "monthly log 2026-05",
          "quote": "opening 8 + bought 26 - closing 10",
          "role": "quantity"
         }
        ],
        "tco2": 71.64
       },
       {
        "basis": "actual 1.9 tCO2/t Verification report RSR-2026-031 (demo)",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0412 180.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_1.txt",
          "quote": "Steel (t): 180",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 342.0
       },
       {
        "basis": "actual 1.9 tCO2/t Verification report RSR-2026-031 (demo)",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0419 170.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_2.txt",
          "quote": "Steel (t): 170",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 323.0
       },
       {
        "basis": "actual 1.9 tCO2/t Verification report RSR-2026-031 (demo)",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0533 160.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_3.txt",
          "quote": "Steel (t): 160",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 304.0
       },
       {
        "basis": "actual 1.9 tCO2/t Verification report RSR-2026-031 (demo)",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0610 150.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_4.txt",
          "quote": "Steel (t): 150",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 285.0
       },
       {
        "basis": "actual 2.1 tCO2/t Verification report KIS-2026-114 (demo)",
        "item": "steel Kaveri Integrated Steel heat KIS-H88213 200.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_5.txt",
          "quote": "Steel (t): 200",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 420.0
       },
       {
        "basis": "actual 2.1 tCO2/t Verification report KIS-2026-114 (demo)",
        "item": "steel Kaveri Integrated Steel heat KIS-H88457 180.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "steel_invoice_1.txt",
          "quote": "Steel (t): 180",
          "role": "tonnes"
         },
         {
          "file": "mtc_6.txt",
          "quote": "Quantity: 46 coils",
          "role": "mill"
         }
        ],
        "tco2": 378.0
       },
       {
        "basis": "",
        "item": "output 1000.0 t",
        "kind": "output",
        "sources": [
         {
          "file": "production.txt",
          "quote": "Output (t): 1000",
          "role": "output"
         }
        ],
        "tco2": null
       }
      ],
      "summary": {
       "name": "Sri Venkateswara Fasteners (your plant)",
       "output_t": 1000.0,
       "see_direct": 0.18733488,
       "see_precursor": 2.052,
       "see_total": 2.23933488,
       "verified_share": 1.0,
       "year": 2032
      }
     },
     "plants": [
      {
       "id": "A",
       "name": "Sri Venkateswara Fasteners (your plant)",
       "see_direct": 0.18733488,
       "see_precursor": 2.052,
       "see_total": 2.23933488,
       "verified_share": 1.0
      },
      {
       "id": "B",
       "name": "Chennai Bolt Works",
       "see_direct": 0.13776923076923075,
       "see_precursor": 2.0,
       "see_total": 2.137769230769231,
       "verified_share": 1.0
      },
      {
       "id": "C",
       "name": "Hyderabad Wire & Fasteners",
       "see_direct": 0.15546875,
       "see_precursor": 1.9791666666666667,
       "see_total": 2.134635416666667,
       "verified_share": 1.0
      },
      {
       "id": "D",
       "name": "Nellore Screws",
       "see_direct": 0.1053529411764706,
       "see_precursor": 3.583823529411765,
       "see_total": 3.6891764705882353,
       "verified_share": 0.5714285714285714
      }
     ]
    },
    "2033": {
     "audit": {
      "checks": [],
      "default_note": "Steel default used: 4.3 tCO2/t before the mark-up. Secondary source. Check it against the current EU table.",
      "draft": "Draft. Not verified. Indirect emissions are not counted for iron and steel goods.",
      "method": [
       "Installation: Sri Venkateswara Fasteners (your plant)",
       "Goods: screws, bolts and nuts (CN 7318)",
       "Route: wire rod, cold heading, heat treatment, plating",
       "Method: calculation-based. Activity data x standard emission factor. Direct emissions only.",
       "diesel: purchase invoices only.",
       "lpg: used = opening stock + purchases - closing stock, logged monthly (2026-04 to 2026-05). Measured by: Weighbridge WB-2, calibrated 2026-01.",
       "Output: dispatch records.",
       "Precursor steel from Kaveri Integrated Steel: verified actual value.",
       "Precursor steel from Rayalaseema Steel Rolling: verified actual value."
      ],
      "plan": {
       "gaps": [
        "diesel: only purchase invoices. Purchases are not usage. Start a monthly stock log.",
        "lpg: 2 of 12 months logged.",
        "Output: no monthly production log. Log tonnes made each month."
       ],
       "lines": [
        "Installation: Sri Venkateswara Fasteners (your plant)",
        "Goods: screws, bolts and nuts (CN 7318)",
        "Route: wire rod, cold heading, heat treatment, plating",
        "Method: calculation-based. Activity data x standard emission factor. Direct emissions only.",
        "diesel: purchase invoices only.",
        "lpg: used = opening stock + purchases - closing stock, logged monthly (2026-04 to 2026-05). Measured by: Weighbridge WB-2, calibrated 2026-01.",
        "Output: dispatch records.",
        "Precursor steel from Kaveri Integrated Steel: verified actual value.",
        "Precursor steel from Rayalaseema Steel Rolling: verified actual value."
       ]
      },
      "rows": [
       {
        "basis": "actual",
        "item": "fuel diesel 12000.0 litre",
        "kind": "fuel",
        "sources": [
         {
          "file": "fuel_3.txt",
          "quote": "Quantity: 12000 litre",
          "role": "quantity"
         }
        ],
        "tco2": 32.115
       },
       {
        "basis": "actual",
        "item": "fuel lpg 28 t",
        "kind": "fuel",
        "sources": [
         {
          "file": "monthly log 2026-04",
          "quote": "opening 6 + bought 30 - closing 8",
          "role": "quantity"
         }
        ],
        "tco2": 83.58
       },
       {
        "basis": "actual",
        "item": "fuel lpg 24 t",
        "kind": "fuel",
        "sources": [
         {
          "file": "monthly log 2026-05",
          "quote": "opening 8 + bought 26 - closing 10",
          "role": "quantity"
         }
        ],
        "tco2": 71.64
       },
       {
        "basis": "actual 1.9 tCO2/t Verification report RSR-2026-031 (demo)",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0412 180.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_1.txt",
          "quote": "Steel (t): 180",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 342.0
       },
       {
        "basis": "actual 1.9 tCO2/t Verification report RSR-2026-031 (demo)",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0419 170.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_2.txt",
          "quote": "Steel (t): 170",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 323.0
       },
       {
        "basis": "actual 1.9 tCO2/t Verification report RSR-2026-031 (demo)",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0533 160.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_3.txt",
          "quote": "Steel (t): 160",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 304.0
       },
       {
        "basis": "actual 1.9 tCO2/t Verification report RSR-2026-031 (demo)",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0610 150.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_4.txt",
          "quote": "Steel (t): 150",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 285.0
       },
       {
        "basis": "actual 2.1 tCO2/t Verification report KIS-2026-114 (demo)",
        "item": "steel Kaveri Integrated Steel heat KIS-H88213 200.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_5.txt",
          "quote": "Steel (t): 200",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 420.0
       },
       {
        "basis": "actual 2.1 tCO2/t Verification report KIS-2026-114 (demo)",
        "item": "steel Kaveri Integrated Steel heat KIS-H88457 180.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "steel_invoice_1.txt",
          "quote": "Steel (t): 180",
          "role": "tonnes"
         },
         {
          "file": "mtc_6.txt",
          "quote": "Quantity: 46 coils",
          "role": "mill"
         }
        ],
        "tco2": 378.0
       },
       {
        "basis": "",
        "item": "output 1000.0 t",
        "kind": "output",
        "sources": [
         {
          "file": "production.txt",
          "quote": "Output (t): 1000",
          "role": "output"
         }
        ],
        "tco2": null
       }
      ],
      "summary": {
       "name": "Sri Venkateswara Fasteners (your plant)",
       "output_t": 1000.0,
       "see_direct": 0.18733488,
       "see_precursor": 2.052,
       "see_total": 2.23933488,
       "verified_share": 1.0,
       "year": 2033
      }
     },
     "plants": [
      {
       "id": "A",
       "name": "Sri Venkateswara Fasteners (your plant)",
       "see_direct": 0.18733488,
       "see_precursor": 2.052,
       "see_total": 2.23933488,
       "verified_share": 1.0
      },
      {
       "id": "B",
       "name": "Chennai Bolt Works",
       "see_direct": 0.13776923076923075,
       "see_precursor": 2.0,
       "see_total": 2.137769230769231,
       "verified_share": 1.0
      },
      {
       "id": "C",
       "name": "Hyderabad Wire & Fasteners",
       "see_direct": 0.15546875,
       "see_precursor": 1.9791666666666667,
       "see_total": 2.134635416666667,
       "verified_share": 1.0
      },
      {
       "id": "D",
       "name": "Nellore Screws",
       "see_direct": 0.1053529411764706,
       "see_precursor": 3.583823529411765,
       "see_total": 3.6891764705882353,
       "verified_share": 0.5714285714285714
      }
     ]
    },
    "2034": {
     "audit": {
      "checks": [],
      "default_note": "Steel default used: 4.3 tCO2/t before the mark-up. Secondary source. Check it against the current EU table.",
      "draft": "Draft. Not verified. Indirect emissions are not counted for iron and steel goods.",
      "method": [
       "Installation: Sri Venkateswara Fasteners (your plant)",
       "Goods: screws, bolts and nuts (CN 7318)",
       "Route: wire rod, cold heading, heat treatment, plating",
       "Method: calculation-based. Activity data x standard emission factor. Direct emissions only.",
       "diesel: purchase invoices only.",
       "lpg: used = opening stock + purchases - closing stock, logged monthly (2026-04 to 2026-05). Measured by: Weighbridge WB-2, calibrated 2026-01.",
       "Output: dispatch records.",
       "Precursor steel from Kaveri Integrated Steel: verified actual value.",
       "Precursor steel from Rayalaseema Steel Rolling: verified actual value."
      ],
      "plan": {
       "gaps": [
        "diesel: only purchase invoices. Purchases are not usage. Start a monthly stock log.",
        "lpg: 2 of 12 months logged.",
        "Output: no monthly production log. Log tonnes made each month."
       ],
       "lines": [
        "Installation: Sri Venkateswara Fasteners (your plant)",
        "Goods: screws, bolts and nuts (CN 7318)",
        "Route: wire rod, cold heading, heat treatment, plating",
        "Method: calculation-based. Activity data x standard emission factor. Direct emissions only.",
        "diesel: purchase invoices only.",
        "lpg: used = opening stock + purchases - closing stock, logged monthly (2026-04 to 2026-05). Measured by: Weighbridge WB-2, calibrated 2026-01.",
        "Output: dispatch records.",
        "Precursor steel from Kaveri Integrated Steel: verified actual value.",
        "Precursor steel from Rayalaseema Steel Rolling: verified actual value."
       ]
      },
      "rows": [
       {
        "basis": "actual",
        "item": "fuel diesel 12000.0 litre",
        "kind": "fuel",
        "sources": [
         {
          "file": "fuel_3.txt",
          "quote": "Quantity: 12000 litre",
          "role": "quantity"
         }
        ],
        "tco2": 32.115
       },
       {
        "basis": "actual",
        "item": "fuel lpg 28 t",
        "kind": "fuel",
        "sources": [
         {
          "file": "monthly log 2026-04",
          "quote": "opening 6 + bought 30 - closing 8",
          "role": "quantity"
         }
        ],
        "tco2": 83.58
       },
       {
        "basis": "actual",
        "item": "fuel lpg 24 t",
        "kind": "fuel",
        "sources": [
         {
          "file": "monthly log 2026-05",
          "quote": "opening 8 + bought 26 - closing 10",
          "role": "quantity"
         }
        ],
        "tco2": 71.64
       },
       {
        "basis": "actual 1.9 tCO2/t Verification report RSR-2026-031 (demo)",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0412 180.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_1.txt",
          "quote": "Steel (t): 180",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 342.0
       },
       {
        "basis": "actual 1.9 tCO2/t Verification report RSR-2026-031 (demo)",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0419 170.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_2.txt",
          "quote": "Steel (t): 170",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 323.0
       },
       {
        "basis": "actual 1.9 tCO2/t Verification report RSR-2026-031 (demo)",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0533 160.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_3.txt",
          "quote": "Steel (t): 160",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 304.0
       },
       {
        "basis": "actual 1.9 tCO2/t Verification report RSR-2026-031 (demo)",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0610 150.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_4.txt",
          "quote": "Steel (t): 150",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 285.0
       },
       {
        "basis": "actual 2.1 tCO2/t Verification report KIS-2026-114 (demo)",
        "item": "steel Kaveri Integrated Steel heat KIS-H88213 200.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_5.txt",
          "quote": "Steel (t): 200",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 420.0
       },
       {
        "basis": "actual 2.1 tCO2/t Verification report KIS-2026-114 (demo)",
        "item": "steel Kaveri Integrated Steel heat KIS-H88457 180.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "steel_invoice_1.txt",
          "quote": "Steel (t): 180",
          "role": "tonnes"
         },
         {
          "file": "mtc_6.txt",
          "quote": "Quantity: 46 coils",
          "role": "mill"
         }
        ],
        "tco2": 378.0
       },
       {
        "basis": "",
        "item": "output 1000.0 t",
        "kind": "output",
        "sources": [
         {
          "file": "production.txt",
          "quote": "Output (t): 1000",
          "role": "output"
         }
        ],
        "tco2": null
       }
      ],
      "summary": {
       "name": "Sri Venkateswara Fasteners (your plant)",
       "output_t": 1000.0,
       "see_direct": 0.18733488,
       "see_precursor": 2.052,
       "see_total": 2.23933488,
       "verified_share": 1.0,
       "year": 2034
      }
     },
     "plants": [
      {
       "id": "A",
       "name": "Sri Venkateswara Fasteners (your plant)",
       "see_direct": 0.18733488,
       "see_precursor": 2.052,
       "see_total": 2.23933488,
       "verified_share": 1.0
      },
      {
       "id": "B",
       "name": "Chennai Bolt Works",
       "see_direct": 0.13776923076923075,
       "see_precursor": 2.0,
       "see_total": 2.137769230769231,
       "verified_share": 1.0
      },
      {
       "id": "C",
       "name": "Hyderabad Wire & Fasteners",
       "see_direct": 0.15546875,
       "see_precursor": 1.9791666666666667,
       "see_total": 2.134635416666667,
       "verified_share": 1.0
      },
      {
       "id": "D",
       "name": "Nellore Screws",
       "see_direct": 0.1053529411764706,
       "see_precursor": 3.583823529411765,
       "see_total": 3.6891764705882353,
       "verified_share": 0.5714285714285714
      }
     ]
    }
   }
  },
  "before": {
   "curve": [
    {
     "default": 9574.752900000001,
     "year": 2026,
     "yours": 7700.877900000001
    },
    {
     "default": 20826.505800000003,
     "year": 2027,
     "yours": 16466.0058
    },
    {
     "default": 45007.01160000001,
     "year": 2028,
     "yours": 35060.5116
    },
    {
     "default": 101265.77610000003,
     "year": 2029,
     "yours": 78886.1511
    },
    {
     "default": 218284.00626000002,
     "year": 2030,
     "yours": 170043.48126
    },
    {
     "default": 274542.77076000004,
     "year": 2031,
     "yours": 213869.12076
    },
    {
     "default": 330801.5352600001,
     "year": 2032,
     "yours": 257694.76025999995
    },
    {
     "default": 387060.29976,
     "year": 2033,
     "yours": 301520.39976
    },
    {
     "default": 450070.11600000004,
     "year": 2034,
     "yours": 350605.11600000004
    }
   ],
   "years": {
    "2026": {
     "audit": {
      "checks": [],
      "default_note": "Steel default used: 4.3 tCO2/t before the mark-up. Secondary source. Check it against the current EU table.",
      "draft": "Draft. Not verified. Indirect emissions are not counted for iron and steel goods.",
      "method": [
       "Installation: Sri Venkateswara Fasteners (your plant)",
       "Goods: screws, bolts and nuts (CN 7318)",
       "Route: wire rod, cold heading, heat treatment, plating",
       "Method: calculation-based. Activity data x standard emission factor. Direct emissions only.",
       "diesel: purchase invoices only.",
       "lpg: used = opening stock + purchases - closing stock, logged monthly (2026-04 to 2026-05). Measured by: Weighbridge WB-2, calibrated 2026-01.",
       "Output: dispatch records.",
       "Precursor steel from Kaveri Integrated Steel: verified actual value.",
       "Precursor steel from Rayalaseema Steel Rolling: EU default value plus penalty."
      ],
      "plan": {
       "gaps": [
        "diesel: only purchase invoices. Purchases are not usage. Start a monthly stock log.",
        "lpg: 2 of 12 months logged.",
        "Output: no monthly production log. Log tonnes made each month.",
        "Rayalaseema Steel Rolling: no verified data. Ask the mill to join."
       ],
       "lines": [
        "Installation: Sri Venkateswara Fasteners (your plant)",
        "Goods: screws, bolts and nuts (CN 7318)",
        "Route: wire rod, cold heading, heat treatment, plating",
        "Method: calculation-based. Activity data x standard emission factor. Direct emissions only.",
        "diesel: purchase invoices only.",
        "lpg: used = opening stock + purchases - closing stock, logged monthly (2026-04 to 2026-05). Measured by: Weighbridge WB-2, calibrated 2026-01.",
        "Output: dispatch records.",
        "Precursor steel from Kaveri Integrated Steel: verified actual value.",
        "Precursor steel from Rayalaseema Steel Rolling: EU default value plus penalty."
       ]
      },
      "rows": [
       {
        "basis": "actual",
        "item": "fuel diesel 12000.0 litre",
        "kind": "fuel",
        "sources": [
         {
          "file": "fuel_3.txt",
          "quote": "Quantity: 12000 litre",
          "role": "quantity"
         }
        ],
        "tco2": 32.115
       },
       {
        "basis": "actual",
        "item": "fuel lpg 28 t",
        "kind": "fuel",
        "sources": [
         {
          "file": "monthly log 2026-04",
          "quote": "opening 6 + bought 30 - closing 8",
          "role": "quantity"
         }
        ],
        "tco2": 83.58
       },
       {
        "basis": "actual",
        "item": "fuel lpg 24 t",
        "kind": "fuel",
        "sources": [
         {
          "file": "monthly log 2026-05",
          "quote": "opening 8 + bought 26 - closing 10",
          "role": "quantity"
         }
        ],
        "tco2": 71.64
       },
       {
        "basis": "default 4.73 tCO2/t",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0412 180.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_1.txt",
          "quote": "Steel (t): 180",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 851.4
       },
       {
        "basis": "default 4.73 tCO2/t",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0419 170.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_2.txt",
          "quote": "Steel (t): 170",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 804.1
       },
       {
        "basis": "default 4.73 tCO2/t",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0533 160.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_3.txt",
          "quote": "Steel (t): 160",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 756.8
       },
       {
        "basis": "default 4.73 tCO2/t",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0610 150.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_4.txt",
          "quote": "Steel (t): 150",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 709.5
       },
       {
        "basis": "actual 2.1 tCO2/t Verification report KIS-2026-114 (demo)",
        "item": "steel Kaveri Integrated Steel heat KIS-H88213 200.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_5.txt",
          "quote": "Steel (t): 200",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 420.0
       },
       {
        "basis": "actual 2.1 tCO2/t Verification report KIS-2026-114 (demo)",
        "item": "steel Kaveri Integrated Steel heat KIS-H88457 180.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "steel_invoice_1.txt",
          "quote": "Steel (t): 180",
          "role": "tonnes"
         },
         {
          "file": "mtc_6.txt",
          "quote": "Quantity: 46 coils",
          "role": "mill"
         }
        ],
        "tco2": 378.0
       },
       {
        "basis": "",
        "item": "output 1000.0 t",
        "kind": "output",
        "sources": [
         {
          "file": "production.txt",
          "quote": "Output (t): 1000",
          "role": "output"
         }
        ],
        "tco2": null
       }
      ],
      "summary": {
       "name": "Sri Venkateswara Fasteners (your plant)",
       "output_t": 1000.0,
       "see_direct": 0.18733488,
       "see_precursor": 3.9198000000000004,
       "see_total": 4.10713488,
       "verified_share": 0.36538461538461536,
       "year": 2026
      }
     },
     "plants": [
      {
       "id": "A",
       "name": "Sri Venkateswara Fasteners (your plant)",
       "see_direct": 0.18733488,
       "see_precursor": 3.9198000000000004,
       "see_total": 4.10713488,
       "verified_share": 0.36538461538461536
      },
      {
       "id": "B",
       "name": "Chennai Bolt Works",
       "see_direct": 0.13776923076923075,
       "see_precursor": 4.176923076923077,
       "see_total": 4.314692307692308,
       "verified_share": 0.25
      },
      {
       "id": "C",
       "name": "Hyderabad Wire & Fasteners",
       "see_direct": 0.15546875,
       "see_precursor": 4.927083333333333,
       "see_total": 5.082552083333334,
       "verified_share": 0.0
      },
      {
       "id": "D",
       "name": "Nellore Screws",
       "see_direct": 0.1053529411764706,
       "see_precursor": 4.869117647058824,
       "see_total": 4.974470588235294,
       "verified_share": 0.0
      }
     ]
    },
    "2027": {
     "audit": {
      "checks": [],
      "default_note": "Steel default used: 4.3 tCO2/t before the mark-up. Secondary source. Check it against the current EU table.",
      "draft": "Draft. Not verified. Indirect emissions are not counted for iron and steel goods.",
      "method": [
       "Installation: Sri Venkateswara Fasteners (your plant)",
       "Goods: screws, bolts and nuts (CN 7318)",
       "Route: wire rod, cold heading, heat treatment, plating",
       "Method: calculation-based. Activity data x standard emission factor. Direct emissions only.",
       "diesel: purchase invoices only.",
       "lpg: used = opening stock + purchases - closing stock, logged monthly (2026-04 to 2026-05). Measured by: Weighbridge WB-2, calibrated 2026-01.",
       "Output: dispatch records.",
       "Precursor steel from Kaveri Integrated Steel: verified actual value.",
       "Precursor steel from Rayalaseema Steel Rolling: EU default value plus penalty."
      ],
      "plan": {
       "gaps": [
        "diesel: only purchase invoices. Purchases are not usage. Start a monthly stock log.",
        "lpg: 2 of 12 months logged.",
        "Output: no monthly production log. Log tonnes made each month.",
        "Rayalaseema Steel Rolling: no verified data. Ask the mill to join."
       ],
       "lines": [
        "Installation: Sri Venkateswara Fasteners (your plant)",
        "Goods: screws, bolts and nuts (CN 7318)",
        "Route: wire rod, cold heading, heat treatment, plating",
        "Method: calculation-based. Activity data x standard emission factor. Direct emissions only.",
        "diesel: purchase invoices only.",
        "lpg: used = opening stock + purchases - closing stock, logged monthly (2026-04 to 2026-05). Measured by: Weighbridge WB-2, calibrated 2026-01.",
        "Output: dispatch records.",
        "Precursor steel from Kaveri Integrated Steel: verified actual value.",
        "Precursor steel from Rayalaseema Steel Rolling: EU default value plus penalty."
       ]
      },
      "rows": [
       {
        "basis": "actual",
        "item": "fuel diesel 12000.0 litre",
        "kind": "fuel",
        "sources": [
         {
          "file": "fuel_3.txt",
          "quote": "Quantity: 12000 litre",
          "role": "quantity"
         }
        ],
        "tco2": 32.115
       },
       {
        "basis": "actual",
        "item": "fuel lpg 28 t",
        "kind": "fuel",
        "sources": [
         {
          "file": "monthly log 2026-04",
          "quote": "opening 6 + bought 30 - closing 8",
          "role": "quantity"
         }
        ],
        "tco2": 83.58
       },
       {
        "basis": "actual",
        "item": "fuel lpg 24 t",
        "kind": "fuel",
        "sources": [
         {
          "file": "monthly log 2026-05",
          "quote": "opening 8 + bought 26 - closing 10",
          "role": "quantity"
         }
        ],
        "tco2": 71.64
       },
       {
        "basis": "default 5.16 tCO2/t",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0412 180.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_1.txt",
          "quote": "Steel (t): 180",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 928.8
       },
       {
        "basis": "default 5.16 tCO2/t",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0419 170.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_2.txt",
          "quote": "Steel (t): 170",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 877.2
       },
       {
        "basis": "default 5.16 tCO2/t",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0533 160.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_3.txt",
          "quote": "Steel (t): 160",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 825.6
       },
       {
        "basis": "default 5.16 tCO2/t",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0610 150.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_4.txt",
          "quote": "Steel (t): 150",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 774.0
       },
       {
        "basis": "actual 2.1 tCO2/t Verification report KIS-2026-114 (demo)",
        "item": "steel Kaveri Integrated Steel heat KIS-H88213 200.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_5.txt",
          "quote": "Steel (t): 200",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 420.0
       },
       {
        "basis": "actual 2.1 tCO2/t Verification report KIS-2026-114 (demo)",
        "item": "steel Kaveri Integrated Steel heat KIS-H88457 180.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "steel_invoice_1.txt",
          "quote": "Steel (t): 180",
          "role": "tonnes"
         },
         {
          "file": "mtc_6.txt",
          "quote": "Quantity: 46 coils",
          "role": "mill"
         }
        ],
        "tco2": 378.0
       },
       {
        "basis": "",
        "item": "output 1000.0 t",
        "kind": "output",
        "sources": [
         {
          "file": "production.txt",
          "quote": "Output (t): 1000",
          "role": "output"
         }
        ],
        "tco2": null
       }
      ],
      "summary": {
       "name": "Sri Venkateswara Fasteners (your plant)",
       "output_t": 1000.0,
       "see_direct": 0.18733488,
       "see_precursor": 4.2036,
       "see_total": 4.39093488,
       "verified_share": 0.36538461538461536,
       "year": 2027
      }
     },
     "plants": [
      {
       "id": "A",
       "name": "Sri Venkateswara Fasteners (your plant)",
       "see_direct": 0.18733488,
       "see_precursor": 4.2036,
       "see_total": 4.39093488,
       "verified_share": 0.36538461538461536
      },
      {
       "id": "B",
       "name": "Chennai Bolt Works",
       "see_direct": 0.13776923076923075,
       "see_precursor": 4.507692307692307,
       "see_total": 4.645461538461538,
       "verified_share": 0.25
      },
      {
       "id": "C",
       "name": "Hyderabad Wire & Fasteners",
       "see_direct": 0.15546875,
       "see_precursor": 5.374999999999999,
       "see_total": 5.530468749999999,
       "verified_share": 0.0
      },
      {
       "id": "D",
       "name": "Nellore Screws",
       "see_direct": 0.1053529411764706,
       "see_precursor": 5.311764705882352,
       "see_total": 5.417117647058822,
       "verified_share": 0.0
      }
     ]
    },
    "2028": {
     "audit": {
      "checks": [],
      "default_note": "Steel default used: 4.3 tCO2/t before the mark-up. Secondary source. Check it against the current EU table.",
      "draft": "Draft. Not verified. Indirect emissions are not counted for iron and steel goods.",
      "method": [
       "Installation: Sri Venkateswara Fasteners (your plant)",
       "Goods: screws, bolts and nuts (CN 7318)",
       "Route: wire rod, cold heading, heat treatment, plating",
       "Method: calculation-based. Activity data x standard emission factor. Direct emissions only.",
       "diesel: purchase invoices only.",
       "lpg: used = opening stock + purchases - closing stock, logged monthly (2026-04 to 2026-05). Measured by: Weighbridge WB-2, calibrated 2026-01.",
       "Output: dispatch records.",
       "Precursor steel from Kaveri Integrated Steel: verified actual value.",
       "Precursor steel from Rayalaseema Steel Rolling: EU default value plus penalty."
      ],
      "plan": {
       "gaps": [
        "diesel: only purchase invoices. Purchases are not usage. Start a monthly stock log.",
        "lpg: 2 of 12 months logged.",
        "Output: no monthly production log. Log tonnes made each month.",
        "Rayalaseema Steel Rolling: no verified data. Ask the mill to join."
       ],
       "lines": [
        "Installation: Sri Venkateswara Fasteners (your plant)",
        "Goods: screws, bolts and nuts (CN 7318)",
        "Route: wire rod, cold heading, heat treatment, plating",
        "Method: calculation-based. Activity data x standard emission factor. Direct emissions only.",
        "diesel: purchase invoices only.",
        "lpg: used = opening stock + purchases - closing stock, logged monthly (2026-04 to 2026-05). Measured by: Weighbridge WB-2, calibrated 2026-01.",
        "Output: dispatch records.",
        "Precursor steel from Kaveri Integrated Steel: verified actual value.",
        "Precursor steel from Rayalaseema Steel Rolling: EU default value plus penalty."
       ]
      },
      "rows": [
       {
        "basis": "actual",
        "item": "fuel diesel 12000.0 litre",
        "kind": "fuel",
        "sources": [
         {
          "file": "fuel_3.txt",
          "quote": "Quantity: 12000 litre",
          "role": "quantity"
         }
        ],
        "tco2": 32.115
       },
       {
        "basis": "actual",
        "item": "fuel lpg 28 t",
        "kind": "fuel",
        "sources": [
         {
          "file": "monthly log 2026-04",
          "quote": "opening 6 + bought 30 - closing 8",
          "role": "quantity"
         }
        ],
        "tco2": 83.58
       },
       {
        "basis": "actual",
        "item": "fuel lpg 24 t",
        "kind": "fuel",
        "sources": [
         {
          "file": "monthly log 2026-05",
          "quote": "opening 8 + bought 26 - closing 10",
          "role": "quantity"
         }
        ],
        "tco2": 71.64
       },
       {
        "basis": "default 5.59 tCO2/t",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0412 180.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_1.txt",
          "quote": "Steel (t): 180",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 1006.2
       },
       {
        "basis": "default 5.59 tCO2/t",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0419 170.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_2.txt",
          "quote": "Steel (t): 170",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 950.3
       },
       {
        "basis": "default 5.59 tCO2/t",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0533 160.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_3.txt",
          "quote": "Steel (t): 160",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 894.4
       },
       {
        "basis": "default 5.59 tCO2/t",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0610 150.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_4.txt",
          "quote": "Steel (t): 150",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 838.5
       },
       {
        "basis": "actual 2.1 tCO2/t Verification report KIS-2026-114 (demo)",
        "item": "steel Kaveri Integrated Steel heat KIS-H88213 200.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_5.txt",
          "quote": "Steel (t): 200",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 420.0
       },
       {
        "basis": "actual 2.1 tCO2/t Verification report KIS-2026-114 (demo)",
        "item": "steel Kaveri Integrated Steel heat KIS-H88457 180.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "steel_invoice_1.txt",
          "quote": "Steel (t): 180",
          "role": "tonnes"
         },
         {
          "file": "mtc_6.txt",
          "quote": "Quantity: 46 coils",
          "role": "mill"
         }
        ],
        "tco2": 378.0
       },
       {
        "basis": "",
        "item": "output 1000.0 t",
        "kind": "output",
        "sources": [
         {
          "file": "production.txt",
          "quote": "Output (t): 1000",
          "role": "output"
         }
        ],
        "tco2": null
       }
      ],
      "summary": {
       "name": "Sri Venkateswara Fasteners (your plant)",
       "output_t": 1000.0,
       "see_direct": 0.18733488,
       "see_precursor": 4.4874,
       "see_total": 4.67473488,
       "verified_share": 0.36538461538461536,
       "year": 2028
      }
     },
     "plants": [
      {
       "id": "A",
       "name": "Sri Venkateswara Fasteners (your plant)",
       "see_direct": 0.18733488,
       "see_precursor": 4.4874,
       "see_total": 4.67473488,
       "verified_share": 0.36538461538461536
      },
      {
       "id": "B",
       "name": "Chennai Bolt Works",
       "see_direct": 0.13776923076923075,
       "see_precursor": 4.838461538461538,
       "see_total": 4.976230769230769,
       "verified_share": 0.25
      },
      {
       "id": "C",
       "name": "Hyderabad Wire & Fasteners",
       "see_direct": 0.15546875,
       "see_precursor": 5.822916666666667,
       "see_total": 5.978385416666667,
       "verified_share": 0.0
      },
      {
       "id": "D",
       "name": "Nellore Screws",
       "see_direct": 0.1053529411764706,
       "see_precursor": 5.754411764705883,
       "see_total": 5.859764705882353,
       "verified_share": 0.0
      }
     ]
    },
    "2029": {
     "audit": {
      "checks": [],
      "default_note": "Steel default used: 4.3 tCO2/t before the mark-up. Secondary source. Check it against the current EU table.",
      "draft": "Draft. Not verified. Indirect emissions are not counted for iron and steel goods.",
      "method": [
       "Installation: Sri Venkateswara Fasteners (your plant)",
       "Goods: screws, bolts and nuts (CN 7318)",
       "Route: wire rod, cold heading, heat treatment, plating",
       "Method: calculation-based. Activity data x standard emission factor. Direct emissions only.",
       "diesel: purchase invoices only.",
       "lpg: used = opening stock + purchases - closing stock, logged monthly (2026-04 to 2026-05). Measured by: Weighbridge WB-2, calibrated 2026-01.",
       "Output: dispatch records.",
       "Precursor steel from Kaveri Integrated Steel: verified actual value.",
       "Precursor steel from Rayalaseema Steel Rolling: EU default value plus penalty."
      ],
      "plan": {
       "gaps": [
        "diesel: only purchase invoices. Purchases are not usage. Start a monthly stock log.",
        "lpg: 2 of 12 months logged.",
        "Output: no monthly production log. Log tonnes made each month.",
        "Rayalaseema Steel Rolling: no verified data. Ask the mill to join."
       ],
       "lines": [
        "Installation: Sri Venkateswara Fasteners (your plant)",
        "Goods: screws, bolts and nuts (CN 7318)",
        "Route: wire rod, cold heading, heat treatment, plating",
        "Method: calculation-based. Activity data x standard emission factor. Direct emissions only.",
        "diesel: purchase invoices only.",
        "lpg: used = opening stock + purchases - closing stock, logged monthly (2026-04 to 2026-05). Measured by: Weighbridge WB-2, calibrated 2026-01.",
        "Output: dispatch records.",
        "Precursor steel from Kaveri Integrated Steel: verified actual value.",
        "Precursor steel from Rayalaseema Steel Rolling: EU default value plus penalty."
       ]
      },
      "rows": [
       {
        "basis": "actual",
        "item": "fuel diesel 12000.0 litre",
        "kind": "fuel",
        "sources": [
         {
          "file": "fuel_3.txt",
          "quote": "Quantity: 12000 litre",
          "role": "quantity"
         }
        ],
        "tco2": 32.115
       },
       {
        "basis": "actual",
        "item": "fuel lpg 28 t",
        "kind": "fuel",
        "sources": [
         {
          "file": "monthly log 2026-04",
          "quote": "opening 6 + bought 30 - closing 8",
          "role": "quantity"
         }
        ],
        "tco2": 83.58
       },
       {
        "basis": "actual",
        "item": "fuel lpg 24 t",
        "kind": "fuel",
        "sources": [
         {
          "file": "monthly log 2026-05",
          "quote": "opening 8 + bought 26 - closing 10",
          "role": "quantity"
         }
        ],
        "tco2": 71.64
       },
       {
        "basis": "default 5.59 tCO2/t",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0412 180.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_1.txt",
          "quote": "Steel (t): 180",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 1006.2
       },
       {
        "basis": "default 5.59 tCO2/t",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0419 170.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_2.txt",
          "quote": "Steel (t): 170",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 950.3
       },
       {
        "basis": "default 5.59 tCO2/t",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0533 160.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_3.txt",
          "quote": "Steel (t): 160",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 894.4
       },
       {
        "basis": "default 5.59 tCO2/t",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0610 150.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_4.txt",
          "quote": "Steel (t): 150",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 838.5
       },
       {
        "basis": "actual 2.1 tCO2/t Verification report KIS-2026-114 (demo)",
        "item": "steel Kaveri Integrated Steel heat KIS-H88213 200.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_5.txt",
          "quote": "Steel (t): 200",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 420.0
       },
       {
        "basis": "actual 2.1 tCO2/t Verification report KIS-2026-114 (demo)",
        "item": "steel Kaveri Integrated Steel heat KIS-H88457 180.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "steel_invoice_1.txt",
          "quote": "Steel (t): 180",
          "role": "tonnes"
         },
         {
          "file": "mtc_6.txt",
          "quote": "Quantity: 46 coils",
          "role": "mill"
         }
        ],
        "tco2": 378.0
       },
       {
        "basis": "",
        "item": "output 1000.0 t",
        "kind": "output",
        "sources": [
         {
          "file": "production.txt",
          "quote": "Output (t): 1000",
          "role": "output"
         }
        ],
        "tco2": null
       }
      ],
      "summary": {
       "name": "Sri Venkateswara Fasteners (your plant)",
       "output_t": 1000.0,
       "see_direct": 0.18733488,
       "see_precursor": 4.4874,
       "see_total": 4.67473488,
       "verified_share": 0.36538461538461536,
       "year": 2029
      }
     },
     "plants": [
      {
       "id": "A",
       "name": "Sri Venkateswara Fasteners (your plant)",
       "see_direct": 0.18733488,
       "see_precursor": 4.4874,
       "see_total": 4.67473488,
       "verified_share": 0.36538461538461536
      },
      {
       "id": "B",
       "name": "Chennai Bolt Works",
       "see_direct": 0.13776923076923075,
       "see_precursor": 4.838461538461538,
       "see_total": 4.976230769230769,
       "verified_share": 0.25
      },
      {
       "id": "C",
       "name": "Hyderabad Wire & Fasteners",
       "see_direct": 0.15546875,
       "see_precursor": 5.822916666666667,
       "see_total": 5.978385416666667,
       "verified_share": 0.0
      },
      {
       "id": "D",
       "name": "Nellore Screws",
       "see_direct": 0.1053529411764706,
       "see_precursor": 5.754411764705883,
       "see_total": 5.859764705882353,
       "verified_share": 0.0
      }
     ]
    },
    "2030": {
     "audit": {
      "checks": [],
      "default_note": "Steel default used: 4.3 tCO2/t before the mark-up. Secondary source. Check it against the current EU table.",
      "draft": "Draft. Not verified. Indirect emissions are not counted for iron and steel goods.",
      "method": [
       "Installation: Sri Venkateswara Fasteners (your plant)",
       "Goods: screws, bolts and nuts (CN 7318)",
       "Route: wire rod, cold heading, heat treatment, plating",
       "Method: calculation-based. Activity data x standard emission factor. Direct emissions only.",
       "diesel: purchase invoices only.",
       "lpg: used = opening stock + purchases - closing stock, logged monthly (2026-04 to 2026-05). Measured by: Weighbridge WB-2, calibrated 2026-01.",
       "Output: dispatch records.",
       "Precursor steel from Kaveri Integrated Steel: verified actual value.",
       "Precursor steel from Rayalaseema Steel Rolling: EU default value plus penalty."
      ],
      "plan": {
       "gaps": [
        "diesel: only purchase invoices. Purchases are not usage. Start a monthly stock log.",
        "lpg: 2 of 12 months logged.",
        "Output: no monthly production log. Log tonnes made each month.",
        "Rayalaseema Steel Rolling: no verified data. Ask the mill to join."
       ],
       "lines": [
        "Installation: Sri Venkateswara Fasteners (your plant)",
        "Goods: screws, bolts and nuts (CN 7318)",
        "Route: wire rod, cold heading, heat treatment, plating",
        "Method: calculation-based. Activity data x standard emission factor. Direct emissions only.",
        "diesel: purchase invoices only.",
        "lpg: used = opening stock + purchases - closing stock, logged monthly (2026-04 to 2026-05). Measured by: Weighbridge WB-2, calibrated 2026-01.",
        "Output: dispatch records.",
        "Precursor steel from Kaveri Integrated Steel: verified actual value.",
        "Precursor steel from Rayalaseema Steel Rolling: EU default value plus penalty."
       ]
      },
      "rows": [
       {
        "basis": "actual",
        "item": "fuel diesel 12000.0 litre",
        "kind": "fuel",
        "sources": [
         {
          "file": "fuel_3.txt",
          "quote": "Quantity: 12000 litre",
          "role": "quantity"
         }
        ],
        "tco2": 32.115
       },
       {
        "basis": "actual",
        "item": "fuel lpg 28 t",
        "kind": "fuel",
        "sources": [
         {
          "file": "monthly log 2026-04",
          "quote": "opening 6 + bought 30 - closing 8",
          "role": "quantity"
         }
        ],
        "tco2": 83.58
       },
       {
        "basis": "actual",
        "item": "fuel lpg 24 t",
        "kind": "fuel",
        "sources": [
         {
          "file": "monthly log 2026-05",
          "quote": "opening 8 + bought 26 - closing 10",
          "role": "quantity"
         }
        ],
        "tco2": 71.64
       },
       {
        "basis": "default 5.59 tCO2/t",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0412 180.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_1.txt",
          "quote": "Steel (t): 180",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 1006.2
       },
       {
        "basis": "default 5.59 tCO2/t",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0419 170.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_2.txt",
          "quote": "Steel (t): 170",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 950.3
       },
       {
        "basis": "default 5.59 tCO2/t",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0533 160.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_3.txt",
          "quote": "Steel (t): 160",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 894.4
       },
       {
        "basis": "default 5.59 tCO2/t",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0610 150.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_4.txt",
          "quote": "Steel (t): 150",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 838.5
       },
       {
        "basis": "actual 2.1 tCO2/t Verification report KIS-2026-114 (demo)",
        "item": "steel Kaveri Integrated Steel heat KIS-H88213 200.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_5.txt",
          "quote": "Steel (t): 200",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 420.0
       },
       {
        "basis": "actual 2.1 tCO2/t Verification report KIS-2026-114 (demo)",
        "item": "steel Kaveri Integrated Steel heat KIS-H88457 180.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "steel_invoice_1.txt",
          "quote": "Steel (t): 180",
          "role": "tonnes"
         },
         {
          "file": "mtc_6.txt",
          "quote": "Quantity: 46 coils",
          "role": "mill"
         }
        ],
        "tco2": 378.0
       },
       {
        "basis": "",
        "item": "output 1000.0 t",
        "kind": "output",
        "sources": [
         {
          "file": "production.txt",
          "quote": "Output (t): 1000",
          "role": "output"
         }
        ],
        "tco2": null
       }
      ],
      "summary": {
       "name": "Sri Venkateswara Fasteners (your plant)",
       "output_t": 1000.0,
       "see_direct": 0.18733488,
       "see_precursor": 4.4874,
       "see_total": 4.67473488,
       "verified_share": 0.36538461538461536,
       "year": 2030
      }
     },
     "plants": [
      {
       "id": "A",
       "name": "Sri Venkateswara Fasteners (your plant)",
       "see_direct": 0.18733488,
       "see_precursor": 4.4874,
       "see_total": 4.67473488,
       "verified_share": 0.36538461538461536
      },
      {
       "id": "B",
       "name": "Chennai Bolt Works",
       "see_direct": 0.13776923076923075,
       "see_precursor": 4.838461538461538,
       "see_total": 4.976230769230769,
       "verified_share": 0.25
      },
      {
       "id": "C",
       "name": "Hyderabad Wire & Fasteners",
       "see_direct": 0.15546875,
       "see_precursor": 5.822916666666667,
       "see_total": 5.978385416666667,
       "verified_share": 0.0
      },
      {
       "id": "D",
       "name": "Nellore Screws",
       "see_direct": 0.1053529411764706,
       "see_precursor": 5.754411764705883,
       "see_total": 5.859764705882353,
       "verified_share": 0.0
      }
     ]
    },
    "2031": {
     "audit": {
      "checks": [],
      "default_note": "Steel default used: 4.3 tCO2/t before the mark-up. Secondary source. Check it against the current EU table.",
      "draft": "Draft. Not verified. Indirect emissions are not counted for iron and steel goods.",
      "method": [
       "Installation: Sri Venkateswara Fasteners (your plant)",
       "Goods: screws, bolts and nuts (CN 7318)",
       "Route: wire rod, cold heading, heat treatment, plating",
       "Method: calculation-based. Activity data x standard emission factor. Direct emissions only.",
       "diesel: purchase invoices only.",
       "lpg: used = opening stock + purchases - closing stock, logged monthly (2026-04 to 2026-05). Measured by: Weighbridge WB-2, calibrated 2026-01.",
       "Output: dispatch records.",
       "Precursor steel from Kaveri Integrated Steel: verified actual value.",
       "Precursor steel from Rayalaseema Steel Rolling: EU default value plus penalty."
      ],
      "plan": {
       "gaps": [
        "diesel: only purchase invoices. Purchases are not usage. Start a monthly stock log.",
        "lpg: 2 of 12 months logged.",
        "Output: no monthly production log. Log tonnes made each month.",
        "Rayalaseema Steel Rolling: no verified data. Ask the mill to join."
       ],
       "lines": [
        "Installation: Sri Venkateswara Fasteners (your plant)",
        "Goods: screws, bolts and nuts (CN 7318)",
        "Route: wire rod, cold heading, heat treatment, plating",
        "Method: calculation-based. Activity data x standard emission factor. Direct emissions only.",
        "diesel: purchase invoices only.",
        "lpg: used = opening stock + purchases - closing stock, logged monthly (2026-04 to 2026-05). Measured by: Weighbridge WB-2, calibrated 2026-01.",
        "Output: dispatch records.",
        "Precursor steel from Kaveri Integrated Steel: verified actual value.",
        "Precursor steel from Rayalaseema Steel Rolling: EU default value plus penalty."
       ]
      },
      "rows": [
       {
        "basis": "actual",
        "item": "fuel diesel 12000.0 litre",
        "kind": "fuel",
        "sources": [
         {
          "file": "fuel_3.txt",
          "quote": "Quantity: 12000 litre",
          "role": "quantity"
         }
        ],
        "tco2": 32.115
       },
       {
        "basis": "actual",
        "item": "fuel lpg 28 t",
        "kind": "fuel",
        "sources": [
         {
          "file": "monthly log 2026-04",
          "quote": "opening 6 + bought 30 - closing 8",
          "role": "quantity"
         }
        ],
        "tco2": 83.58
       },
       {
        "basis": "actual",
        "item": "fuel lpg 24 t",
        "kind": "fuel",
        "sources": [
         {
          "file": "monthly log 2026-05",
          "quote": "opening 8 + bought 26 - closing 10",
          "role": "quantity"
         }
        ],
        "tco2": 71.64
       },
       {
        "basis": "default 5.59 tCO2/t",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0412 180.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_1.txt",
          "quote": "Steel (t): 180",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 1006.2
       },
       {
        "basis": "default 5.59 tCO2/t",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0419 170.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_2.txt",
          "quote": "Steel (t): 170",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 950.3
       },
       {
        "basis": "default 5.59 tCO2/t",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0533 160.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_3.txt",
          "quote": "Steel (t): 160",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 894.4
       },
       {
        "basis": "default 5.59 tCO2/t",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0610 150.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_4.txt",
          "quote": "Steel (t): 150",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 838.5
       },
       {
        "basis": "actual 2.1 tCO2/t Verification report KIS-2026-114 (demo)",
        "item": "steel Kaveri Integrated Steel heat KIS-H88213 200.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_5.txt",
          "quote": "Steel (t): 200",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 420.0
       },
       {
        "basis": "actual 2.1 tCO2/t Verification report KIS-2026-114 (demo)",
        "item": "steel Kaveri Integrated Steel heat KIS-H88457 180.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "steel_invoice_1.txt",
          "quote": "Steel (t): 180",
          "role": "tonnes"
         },
         {
          "file": "mtc_6.txt",
          "quote": "Quantity: 46 coils",
          "role": "mill"
         }
        ],
        "tco2": 378.0
       },
       {
        "basis": "",
        "item": "output 1000.0 t",
        "kind": "output",
        "sources": [
         {
          "file": "production.txt",
          "quote": "Output (t): 1000",
          "role": "output"
         }
        ],
        "tco2": null
       }
      ],
      "summary": {
       "name": "Sri Venkateswara Fasteners (your plant)",
       "output_t": 1000.0,
       "see_direct": 0.18733488,
       "see_precursor": 4.4874,
       "see_total": 4.67473488,
       "verified_share": 0.36538461538461536,
       "year": 2031
      }
     },
     "plants": [
      {
       "id": "A",
       "name": "Sri Venkateswara Fasteners (your plant)",
       "see_direct": 0.18733488,
       "see_precursor": 4.4874,
       "see_total": 4.67473488,
       "verified_share": 0.36538461538461536
      },
      {
       "id": "B",
       "name": "Chennai Bolt Works",
       "see_direct": 0.13776923076923075,
       "see_precursor": 4.838461538461538,
       "see_total": 4.976230769230769,
       "verified_share": 0.25
      },
      {
       "id": "C",
       "name": "Hyderabad Wire & Fasteners",
       "see_direct": 0.15546875,
       "see_precursor": 5.822916666666667,
       "see_total": 5.978385416666667,
       "verified_share": 0.0
      },
      {
       "id": "D",
       "name": "Nellore Screws",
       "see_direct": 0.1053529411764706,
       "see_precursor": 5.754411764705883,
       "see_total": 5.859764705882353,
       "verified_share": 0.0
      }
     ]
    },
    "2032": {
     "audit": {
      "checks": [],
      "default_note": "Steel default used: 4.3 tCO2/t before the mark-up. Secondary source. Check it against the current EU table.",
      "draft": "Draft. Not verified. Indirect emissions are not counted for iron and steel goods.",
      "method": [
       "Installation: Sri Venkateswara Fasteners (your plant)",
       "Goods: screws, bolts and nuts (CN 7318)",
       "Route: wire rod, cold heading, heat treatment, plating",
       "Method: calculation-based. Activity data x standard emission factor. Direct emissions only.",
       "diesel: purchase invoices only.",
       "lpg: used = opening stock + purchases - closing stock, logged monthly (2026-04 to 2026-05). Measured by: Weighbridge WB-2, calibrated 2026-01.",
       "Output: dispatch records.",
       "Precursor steel from Kaveri Integrated Steel: verified actual value.",
       "Precursor steel from Rayalaseema Steel Rolling: EU default value plus penalty."
      ],
      "plan": {
       "gaps": [
        "diesel: only purchase invoices. Purchases are not usage. Start a monthly stock log.",
        "lpg: 2 of 12 months logged.",
        "Output: no monthly production log. Log tonnes made each month.",
        "Rayalaseema Steel Rolling: no verified data. Ask the mill to join."
       ],
       "lines": [
        "Installation: Sri Venkateswara Fasteners (your plant)",
        "Goods: screws, bolts and nuts (CN 7318)",
        "Route: wire rod, cold heading, heat treatment, plating",
        "Method: calculation-based. Activity data x standard emission factor. Direct emissions only.",
        "diesel: purchase invoices only.",
        "lpg: used = opening stock + purchases - closing stock, logged monthly (2026-04 to 2026-05). Measured by: Weighbridge WB-2, calibrated 2026-01.",
        "Output: dispatch records.",
        "Precursor steel from Kaveri Integrated Steel: verified actual value.",
        "Precursor steel from Rayalaseema Steel Rolling: EU default value plus penalty."
       ]
      },
      "rows": [
       {
        "basis": "actual",
        "item": "fuel diesel 12000.0 litre",
        "kind": "fuel",
        "sources": [
         {
          "file": "fuel_3.txt",
          "quote": "Quantity: 12000 litre",
          "role": "quantity"
         }
        ],
        "tco2": 32.115
       },
       {
        "basis": "actual",
        "item": "fuel lpg 28 t",
        "kind": "fuel",
        "sources": [
         {
          "file": "monthly log 2026-04",
          "quote": "opening 6 + bought 30 - closing 8",
          "role": "quantity"
         }
        ],
        "tco2": 83.58
       },
       {
        "basis": "actual",
        "item": "fuel lpg 24 t",
        "kind": "fuel",
        "sources": [
         {
          "file": "monthly log 2026-05",
          "quote": "opening 8 + bought 26 - closing 10",
          "role": "quantity"
         }
        ],
        "tco2": 71.64
       },
       {
        "basis": "default 5.59 tCO2/t",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0412 180.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_1.txt",
          "quote": "Steel (t): 180",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 1006.2
       },
       {
        "basis": "default 5.59 tCO2/t",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0419 170.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_2.txt",
          "quote": "Steel (t): 170",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 950.3
       },
       {
        "basis": "default 5.59 tCO2/t",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0533 160.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_3.txt",
          "quote": "Steel (t): 160",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 894.4
       },
       {
        "basis": "default 5.59 tCO2/t",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0610 150.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_4.txt",
          "quote": "Steel (t): 150",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 838.5
       },
       {
        "basis": "actual 2.1 tCO2/t Verification report KIS-2026-114 (demo)",
        "item": "steel Kaveri Integrated Steel heat KIS-H88213 200.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_5.txt",
          "quote": "Steel (t): 200",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 420.0
       },
       {
        "basis": "actual 2.1 tCO2/t Verification report KIS-2026-114 (demo)",
        "item": "steel Kaveri Integrated Steel heat KIS-H88457 180.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "steel_invoice_1.txt",
          "quote": "Steel (t): 180",
          "role": "tonnes"
         },
         {
          "file": "mtc_6.txt",
          "quote": "Quantity: 46 coils",
          "role": "mill"
         }
        ],
        "tco2": 378.0
       },
       {
        "basis": "",
        "item": "output 1000.0 t",
        "kind": "output",
        "sources": [
         {
          "file": "production.txt",
          "quote": "Output (t): 1000",
          "role": "output"
         }
        ],
        "tco2": null
       }
      ],
      "summary": {
       "name": "Sri Venkateswara Fasteners (your plant)",
       "output_t": 1000.0,
       "see_direct": 0.18733488,
       "see_precursor": 4.4874,
       "see_total": 4.67473488,
       "verified_share": 0.36538461538461536,
       "year": 2032
      }
     },
     "plants": [
      {
       "id": "A",
       "name": "Sri Venkateswara Fasteners (your plant)",
       "see_direct": 0.18733488,
       "see_precursor": 4.4874,
       "see_total": 4.67473488,
       "verified_share": 0.36538461538461536
      },
      {
       "id": "B",
       "name": "Chennai Bolt Works",
       "see_direct": 0.13776923076923075,
       "see_precursor": 4.838461538461538,
       "see_total": 4.976230769230769,
       "verified_share": 0.25
      },
      {
       "id": "C",
       "name": "Hyderabad Wire & Fasteners",
       "see_direct": 0.15546875,
       "see_precursor": 5.822916666666667,
       "see_total": 5.978385416666667,
       "verified_share": 0.0
      },
      {
       "id": "D",
       "name": "Nellore Screws",
       "see_direct": 0.1053529411764706,
       "see_precursor": 5.754411764705883,
       "see_total": 5.859764705882353,
       "verified_share": 0.0
      }
     ]
    },
    "2033": {
     "audit": {
      "checks": [],
      "default_note": "Steel default used: 4.3 tCO2/t before the mark-up. Secondary source. Check it against the current EU table.",
      "draft": "Draft. Not verified. Indirect emissions are not counted for iron and steel goods.",
      "method": [
       "Installation: Sri Venkateswara Fasteners (your plant)",
       "Goods: screws, bolts and nuts (CN 7318)",
       "Route: wire rod, cold heading, heat treatment, plating",
       "Method: calculation-based. Activity data x standard emission factor. Direct emissions only.",
       "diesel: purchase invoices only.",
       "lpg: used = opening stock + purchases - closing stock, logged monthly (2026-04 to 2026-05). Measured by: Weighbridge WB-2, calibrated 2026-01.",
       "Output: dispatch records.",
       "Precursor steel from Kaveri Integrated Steel: verified actual value.",
       "Precursor steel from Rayalaseema Steel Rolling: EU default value plus penalty."
      ],
      "plan": {
       "gaps": [
        "diesel: only purchase invoices. Purchases are not usage. Start a monthly stock log.",
        "lpg: 2 of 12 months logged.",
        "Output: no monthly production log. Log tonnes made each month.",
        "Rayalaseema Steel Rolling: no verified data. Ask the mill to join."
       ],
       "lines": [
        "Installation: Sri Venkateswara Fasteners (your plant)",
        "Goods: screws, bolts and nuts (CN 7318)",
        "Route: wire rod, cold heading, heat treatment, plating",
        "Method: calculation-based. Activity data x standard emission factor. Direct emissions only.",
        "diesel: purchase invoices only.",
        "lpg: used = opening stock + purchases - closing stock, logged monthly (2026-04 to 2026-05). Measured by: Weighbridge WB-2, calibrated 2026-01.",
        "Output: dispatch records.",
        "Precursor steel from Kaveri Integrated Steel: verified actual value.",
        "Precursor steel from Rayalaseema Steel Rolling: EU default value plus penalty."
       ]
      },
      "rows": [
       {
        "basis": "actual",
        "item": "fuel diesel 12000.0 litre",
        "kind": "fuel",
        "sources": [
         {
          "file": "fuel_3.txt",
          "quote": "Quantity: 12000 litre",
          "role": "quantity"
         }
        ],
        "tco2": 32.115
       },
       {
        "basis": "actual",
        "item": "fuel lpg 28 t",
        "kind": "fuel",
        "sources": [
         {
          "file": "monthly log 2026-04",
          "quote": "opening 6 + bought 30 - closing 8",
          "role": "quantity"
         }
        ],
        "tco2": 83.58
       },
       {
        "basis": "actual",
        "item": "fuel lpg 24 t",
        "kind": "fuel",
        "sources": [
         {
          "file": "monthly log 2026-05",
          "quote": "opening 8 + bought 26 - closing 10",
          "role": "quantity"
         }
        ],
        "tco2": 71.64
       },
       {
        "basis": "default 5.59 tCO2/t",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0412 180.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_1.txt",
          "quote": "Steel (t): 180",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 1006.2
       },
       {
        "basis": "default 5.59 tCO2/t",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0419 170.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_2.txt",
          "quote": "Steel (t): 170",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 950.3
       },
       {
        "basis": "default 5.59 tCO2/t",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0533 160.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_3.txt",
          "quote": "Steel (t): 160",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 894.4
       },
       {
        "basis": "default 5.59 tCO2/t",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0610 150.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_4.txt",
          "quote": "Steel (t): 150",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 838.5
       },
       {
        "basis": "actual 2.1 tCO2/t Verification report KIS-2026-114 (demo)",
        "item": "steel Kaveri Integrated Steel heat KIS-H88213 200.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_5.txt",
          "quote": "Steel (t): 200",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 420.0
       },
       {
        "basis": "actual 2.1 tCO2/t Verification report KIS-2026-114 (demo)",
        "item": "steel Kaveri Integrated Steel heat KIS-H88457 180.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "steel_invoice_1.txt",
          "quote": "Steel (t): 180",
          "role": "tonnes"
         },
         {
          "file": "mtc_6.txt",
          "quote": "Quantity: 46 coils",
          "role": "mill"
         }
        ],
        "tco2": 378.0
       },
       {
        "basis": "",
        "item": "output 1000.0 t",
        "kind": "output",
        "sources": [
         {
          "file": "production.txt",
          "quote": "Output (t): 1000",
          "role": "output"
         }
        ],
        "tco2": null
       }
      ],
      "summary": {
       "name": "Sri Venkateswara Fasteners (your plant)",
       "output_t": 1000.0,
       "see_direct": 0.18733488,
       "see_precursor": 4.4874,
       "see_total": 4.67473488,
       "verified_share": 0.36538461538461536,
       "year": 2033
      }
     },
     "plants": [
      {
       "id": "A",
       "name": "Sri Venkateswara Fasteners (your plant)",
       "see_direct": 0.18733488,
       "see_precursor": 4.4874,
       "see_total": 4.67473488,
       "verified_share": 0.36538461538461536
      },
      {
       "id": "B",
       "name": "Chennai Bolt Works",
       "see_direct": 0.13776923076923075,
       "see_precursor": 4.838461538461538,
       "see_total": 4.976230769230769,
       "verified_share": 0.25
      },
      {
       "id": "C",
       "name": "Hyderabad Wire & Fasteners",
       "see_direct": 0.15546875,
       "see_precursor": 5.822916666666667,
       "see_total": 5.978385416666667,
       "verified_share": 0.0
      },
      {
       "id": "D",
       "name": "Nellore Screws",
       "see_direct": 0.1053529411764706,
       "see_precursor": 5.754411764705883,
       "see_total": 5.859764705882353,
       "verified_share": 0.0
      }
     ]
    },
    "2034": {
     "audit": {
      "checks": [],
      "default_note": "Steel default used: 4.3 tCO2/t before the mark-up. Secondary source. Check it against the current EU table.",
      "draft": "Draft. Not verified. Indirect emissions are not counted for iron and steel goods.",
      "method": [
       "Installation: Sri Venkateswara Fasteners (your plant)",
       "Goods: screws, bolts and nuts (CN 7318)",
       "Route: wire rod, cold heading, heat treatment, plating",
       "Method: calculation-based. Activity data x standard emission factor. Direct emissions only.",
       "diesel: purchase invoices only.",
       "lpg: used = opening stock + purchases - closing stock, logged monthly (2026-04 to 2026-05). Measured by: Weighbridge WB-2, calibrated 2026-01.",
       "Output: dispatch records.",
       "Precursor steel from Kaveri Integrated Steel: verified actual value.",
       "Precursor steel from Rayalaseema Steel Rolling: EU default value plus penalty."
      ],
      "plan": {
       "gaps": [
        "diesel: only purchase invoices. Purchases are not usage. Start a monthly stock log.",
        "lpg: 2 of 12 months logged.",
        "Output: no monthly production log. Log tonnes made each month.",
        "Rayalaseema Steel Rolling: no verified data. Ask the mill to join."
       ],
       "lines": [
        "Installation: Sri Venkateswara Fasteners (your plant)",
        "Goods: screws, bolts and nuts (CN 7318)",
        "Route: wire rod, cold heading, heat treatment, plating",
        "Method: calculation-based. Activity data x standard emission factor. Direct emissions only.",
        "diesel: purchase invoices only.",
        "lpg: used = opening stock + purchases - closing stock, logged monthly (2026-04 to 2026-05). Measured by: Weighbridge WB-2, calibrated 2026-01.",
        "Output: dispatch records.",
        "Precursor steel from Kaveri Integrated Steel: verified actual value.",
        "Precursor steel from Rayalaseema Steel Rolling: EU default value plus penalty."
       ]
      },
      "rows": [
       {
        "basis": "actual",
        "item": "fuel diesel 12000.0 litre",
        "kind": "fuel",
        "sources": [
         {
          "file": "fuel_3.txt",
          "quote": "Quantity: 12000 litre",
          "role": "quantity"
         }
        ],
        "tco2": 32.115
       },
       {
        "basis": "actual",
        "item": "fuel lpg 28 t",
        "kind": "fuel",
        "sources": [
         {
          "file": "monthly log 2026-04",
          "quote": "opening 6 + bought 30 - closing 8",
          "role": "quantity"
         }
        ],
        "tco2": 83.58
       },
       {
        "basis": "actual",
        "item": "fuel lpg 24 t",
        "kind": "fuel",
        "sources": [
         {
          "file": "monthly log 2026-05",
          "quote": "opening 8 + bought 26 - closing 10",
          "role": "quantity"
         }
        ],
        "tco2": 71.64
       },
       {
        "basis": "default 5.59 tCO2/t",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0412 180.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_1.txt",
          "quote": "Steel (t): 180",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 1006.2
       },
       {
        "basis": "default 5.59 tCO2/t",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0419 170.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_2.txt",
          "quote": "Steel (t): 170",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 950.3
       },
       {
        "basis": "default 5.59 tCO2/t",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0533 160.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_3.txt",
          "quote": "Steel (t): 160",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 894.4
       },
       {
        "basis": "default 5.59 tCO2/t",
        "item": "steel Rayalaseema Steel Rolling heat RSR-24-0610 150.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_4.txt",
          "quote": "Steel (t): 150",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 838.5
       },
       {
        "basis": "actual 2.1 tCO2/t Verification report KIS-2026-114 (demo)",
        "item": "steel Kaveri Integrated Steel heat KIS-H88213 200.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "mtc_5.txt",
          "quote": "Steel (t): 200",
          "role": "tonnes and mill"
         }
        ],
        "tco2": 420.0
       },
       {
        "basis": "actual 2.1 tCO2/t Verification report KIS-2026-114 (demo)",
        "item": "steel Kaveri Integrated Steel heat KIS-H88457 180.0 t",
        "kind": "steel",
        "sources": [
         {
          "file": "steel_invoice_1.txt",
          "quote": "Steel (t): 180",
          "role": "tonnes"
         },
         {
          "file": "mtc_6.txt",
          "quote": "Quantity: 46 coils",
          "role": "mill"
         }
        ],
        "tco2": 378.0
       },
       {
        "basis": "",
        "item": "output 1000.0 t",
        "kind": "output",
        "sources": [
         {
          "file": "production.txt",
          "quote": "Output (t): 1000",
          "role": "output"
         }
        ],
        "tco2": null
       }
      ],
      "summary": {
       "name": "Sri Venkateswara Fasteners (your plant)",
       "output_t": 1000.0,
       "see_direct": 0.18733488,
       "see_precursor": 4.4874,
       "see_total": 4.67473488,
       "verified_share": 0.36538461538461536,
       "year": 2034
      }
     },
     "plants": [
      {
       "id": "A",
       "name": "Sri Venkateswara Fasteners (your plant)",
       "see_direct": 0.18733488,
       "see_precursor": 4.4874,
       "see_total": 4.67473488,
       "verified_share": 0.36538461538461536
      },
      {
       "id": "B",
       "name": "Chennai Bolt Works",
       "see_direct": 0.13776923076923075,
       "see_precursor": 4.838461538461538,
       "see_total": 4.976230769230769,
       "verified_share": 0.25
      },
      {
       "id": "C",
       "name": "Hyderabad Wire & Fasteners",
       "see_direct": 0.15546875,
       "see_precursor": 5.822916666666667,
       "see_total": 5.978385416666667,
       "verified_share": 0.0
      },
      {
       "id": "D",
       "name": "Nellore Screws",
       "see_direct": 0.1053529411764706,
       "see_precursor": 5.754411764705883,
       "see_total": 5.859764705882353,
       "verified_share": 0.0
      }
     ]
    }
   }
  }
 }
};
