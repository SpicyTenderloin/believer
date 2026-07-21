# Future Capability Roadmap

Capabilities not required for current flight-readiness but planned for later phases of the project. Current build and flight-readiness work is tracked in [`docs/project/build-checklist.md`](build-checklist.md).

| Category | Task | Notes |
|---|---|---|
| Power | Custom power distribution board | Bespoke PDB to replace the Holybro PM03D - see `docs/engineering/requirements/power-distribution-board-requirements.md` |
| Airframe | Launch dolly | Releasable ground-roll launch cart, supplementing the current assisted hand launch - see `docs/engineering/requirements/launch-dolly-requirements.md` |
| Airframe | Parachute/payload bay servo | Install a servo in the parachute bay and wire it for parachute or payload deployment |
| Avionics | Companion computer mount | Design and install a mount for the companion computer inside the airframe |
| Avionics | Camera mount | Design and install a mount for the IMX335 5MP USB camera |
| Payload | Configure camera to record on arm | Configure the companion computer to begin camera recording automatically when the aircraft arms. Blocked by: Companion computer mount, Camera mount |
| Sensors | Source LiDAR | Identify and procure an appropriate LiDAR unit for terrain following, obstacle avoidance, or precision landing |
| Sensors | Install LiDAR | Mount and wire the LiDAR; configure PX4 driver and distance sensor parameters. Blocked by: Source LiDAR |
| Configure and Tune | Configure auto takeoff | Configure and test PX4 hand-launch or runway takeoff procedure for autonomous departure. Blocked by: Install LiDAR |
| Configure and Tune | Configure auto land | Configure and test PX4 automated landing approach and touchdown sequence. Blocked by: Install LiDAR |
