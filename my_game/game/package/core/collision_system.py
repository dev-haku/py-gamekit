from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from .gameobject import Gameobject

if TYPE_CHECKING:
    from .collider import Collider
    from ..components.transform import Transform
   

class CollisionSystem(Gameobject):
    def __init__(self, context):
        super().__init__(context)
        self._collisions: dict[Collider, list[Collider]] = {}

    def update(self):
        self._collisions = self._detect_colliding()

    def get_colliding_colliders(self, collider: Collider) -> list[Collider]:
        return self._collisions.get(collider, [])

    # ビッグオー記法
    # O(SelfObjects * SelfHitboxes * TargetObjects * TargetHitboxes)
    def _detect_colliding(self) -> dict[Collider, list[Collider]]:
        candidates = self._collect_collidables()

        rects_of = {
            collider: [self._create_rect(transform, hb) for hb in collider.hitboxes]
            for collider, transform in candidates
        }

        result: dict[Collider, list[Collider]] = {c: [] for c, _ in candidates}

        for i in range(len(candidates)):
            a_collider = candidates[i][0]
            a_rects = rects_of[a_collider]

            for j in range(i + 1, len(candidates)):
                b_collider = candidates[j][0]
                b_rects = rects_of[b_collider]

                if any(r.collidelist(b_rects) != -1 for r in a_rects):
                    result[a_collider].append(b_collider)
                    result[b_collider].append(a_collider)

        return result

    # 審査: collider と transform をセットでもつ
    def _collect_collidables(self) -> list[tuple[Collider, Transform]]:
        candidates = []
        for go in self.scene.gameobjects:
            
            transform: Transform = go.get_component("Transform")
            collider: Collider = go.get_component("Collider")

            if collider is None or transform is None:
                continue
            
            if collider.active == False or transform.active == False:
                continue

            candidates.append((collider, transform))

        return candidates

    def _create_rect(self, transform, hitbox) -> pygame.Rect:
        pos = (
            transform.position.x + (hitbox.offset_position[0] * transform.scale.x),
            transform.position.y + (hitbox.offset_position[1] * transform.scale.y)
        )

        scaled_size = (
            hitbox.size[0] * transform.scale.x,
            hitbox.size[1] * transform.scale.y
        )

        return pygame.Rect(
            pos[0],
            pos[1],
            scaled_size[0],
            scaled_size[1]
        )