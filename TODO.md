# Next Step Implementation Plan

## ✅ Backend API Additions
- [ ] Add `UpdateShipmentRequest` schema to `app/schemas.py`
- [ ] Add `RegisterRequest` schema to `app/schemas.py`
- [ ] Add `delete_shipment()` function to `app/db.py`
- [ ] Add `update_shipment()` function to `app/db.py`
- [ ] Add `register_user()` function to `app/db.py`
- [ ] Add routes in `app/main.py`: `PUT /shipments/{id}`, `DELETE /shipments/{id}`, `POST /register`, `GET /operations`

## ✅ Frontend Pages
- [ ] Create `app/static/operations.html` — Shipment CRUD management UI
- [ ] Rewrite `app/static/map_tracker.html` — Real Leaflet.js map with routes

## ✅ Navigation
- [ ] Add unified navigation bar to all HTML pages (index.html, dashboard.html, tracker.html, live.html, map_tracker.html, operations.html)

## ✅ Testing
- [ ] Add tests for new endpoints in `tests/test_app.py`

