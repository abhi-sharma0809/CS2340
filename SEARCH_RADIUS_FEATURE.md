# Search Radius Feature

## Overview
The search radius feature now actually filters candidates based on their distance from the search location. Previously, it was just a visual element without functionality.

## How It Works

### Distance Calculation
Uses the **Haversine formula** to calculate the great-circle distance between two points on Earth based on their latitude and longitude coordinates.

### Location Matching

The system uses a **two-tier approach**:

1. **Coordinate-based matching** (preferred):
   - If both search location and candidate location have coordinates, calculates actual distance
   - Only shows candidates within the specified radius
   - Closer candidates get higher match scores
   - Shows actual distance in kilometers in results

2. **Text-based matching** (fallback):
   - If coordinates aren't available, falls back to text matching
   - Matches if location text contains the search term (e.g., "Atlanta" matches "Atlanta, GA")

### Coordinate Sources

The system gets coordinates from two places:

1. **Stored coordinates**: If a candidate has saved `latitude` and `longitude` in their profile
2. **City lookup**: Built-in database of common US cities with coordinates

### Supported Cities (Built-in)

The system has built-in coordinates for these cities:
- Atlanta, GA
- New York, NY
- Los Angeles, CA
- Chicago, IL
- San Francisco, CA
- Boston, MA
- Seattle, WA
- Austin, TX
- Denver, CO
- Miami, FL

**Note**: More cities can be easily added to the `_get_coordinates_from_location()` function.

---

## Features

### 1. Auto-fill Coordinates

When a job seeker enters their location:
- System automatically looks up coordinates for known cities
- Stores coordinates in `latitude` and `longitude` fields
- Happens automatically when saving profile

### 2. Distance-based Scoring

Candidates get scored based on proximity:
- Within radius: Score = 10 - (distance / (radius / 10))
- Closer candidates rank higher in results
- Distance shown in search results (e.g., "Atlanta, GA (23 km away)")

### 3. Radius Options

Recruiters can choose from:
- 25 km
- 50 km (default)
- 100 km
- 200 km

---

## Usage Examples

### Example 1: Exact Match
**Search**: Location: "Atlanta, GA", Radius: 50 km  
**Candidate**: Location: "Atlanta, GA"  
**Result**: ✅ Match! (0 km away) - High score

### Example 2: Within Radius
**Search**: Location: "Atlanta, GA", Radius: 50 km  
**Candidate**: Location: "Marietta, GA" (manually geocoded to ~20km from Atlanta)  
**Result**: ✅ Match! (20 km away) - Medium-high score

### Example 3: Outside Radius
**Search**: Location: "Atlanta, GA", Radius: 50 km  
**Candidate**: Location: "Miami, FL"  
**Result**: ❌ No match (1,190 km away - outside radius)

### Example 4: Fallback Text Matching
**Search**: Location: "Atlanta", Radius: 50 km  
**Candidate**: Location: "Atlanta, Georgia" (no coordinates stored)  
**Result**: ✅ Match! (text-based fallback)

---

## Technical Details

### Files Modified

1. **`jobs/views.py`**:
   - Added `_get_coordinates_from_location()` - City coordinate lookup
   - Added `_calculate_distance()` - Haversine distance formula
   - Updated `candidate_search()` - Location matching with radius filtering
   - Updated location matching logic in search results

2. **`accounts/forms.py`**:
   - Updated `ProfileForm.save()` - Auto-fills coordinates when location is saved

3. **`jobs/templates/jobs/candidate_search.html`**:
   - Added help text explaining radius functionality

### Database Fields Used

- `Profile.location` (CharField) - Text location
- `Profile.latitude` (FloatField) - Latitude coordinate  
- `Profile.longitude` (FloatField) - Longitude coordinate

---

## Haversine Formula

The distance calculation uses the Haversine formula:

```python
def _calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth's radius in km
    
    # Convert to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Differences
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Haversine formula
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c  # Distance in km
```

---

## Adding More Cities

To add more cities to the coordinate lookup, edit `jobs/views.py`:

```python
def _get_coordinates_from_location(location_text):
    city_coordinates = {
        'atlanta': (33.7490, -84.3880),
        'atlanta, ga': (33.7490, -84.3880),
        # Add more cities here:
        'dallas': (32.7767, -96.7970),
        'dallas, tx': (32.7767, -96.7970),
        # ...
    }
    location_lower = location_text.lower().strip()
    return city_coordinates.get(location_lower, (None, None))
```

---

## Future Enhancements

### Option 1: Real Geocoding API
Instead of the built-in city list, integrate with a geocoding service:
- Google Maps Geocoding API
- OpenStreetMap Nominatim
- MapBox Geocoding

Benefits:
- Support any location worldwide
- More accurate coordinates
- Support for street addresses

### Option 2: IP Geolocation
Auto-detect user's location:
- Use IP geolocation on signup
- Ask for permission to use browser location API
- Pre-fill location field

### Option 3: Interactive Map
Add a map interface:
- Visual radius circle on map
- Click to set location
- See candidate density by area

---

## Testing the Feature

### Test Scenario 1: Distance Filtering Works
1. Create job seeker with location "Atlanta, GA"
2. Create another with location "New York, NY"
3. As recruiter, search:
   - Location: "Atlanta, GA"
   - Radius: 50 km
4. **Expected**: Only Atlanta candidate appears

### Test Scenario 2: Distance Display
1. Search with location that has multiple candidates nearby
2. **Expected**: Results show distance (e.g., "23 km away")

### Test Scenario 3: Fallback to Text
1. Create candidate with location "Atlanta, Georgia" (no standard format)
2. Search for "Atlanta"
3. **Expected**: Still matches using text fallback

### Test Scenario 4: Radius Adjustment
1. Search with 25 km radius - note results count
2. Change to 100 km radius - note results count
3. **Expected**: More candidates with larger radius

---

## Troubleshooting

**Problem**: No candidates showing up even though they should match

**Solutions**:
- Check if locations are in the city database
- Verify profile has coordinates (check `latitude` and `longitude` fields)
- Try text-based matching by using partial location names
- Increase the search radius

**Problem**: Wrong distances showing

**Solutions**:
- Verify coordinates are correct in database
- Check that city names match exactly (case-insensitive but spelling matters)
- Ensure coordinates are in decimal degrees format (not DMS)

---

## Summary

✅ **What Changed**:
- Radius now actually filters by distance
- Distance-based scoring prioritizes nearby candidates
- Auto-fills coordinates for known cities
- Shows actual distance in results
- Fallback to text matching when needed

✅ **What Works**:
- Distance calculation using Haversine formula
- Filtering candidates within specified radius
- Proximity-based match scoring
- Text-based fallback for unknown locations
- Works with saved searches and notifications

The search radius is now a fully functional feature that provides real geographic filtering! 🎯

