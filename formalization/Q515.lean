import Std

namespace RectangleCover
/-- Each selected diagonal pair is contained in its assigned product
rectangle. Distinct selected indices forbid an accepted cross pair. -/
theorem selected_injection {I G X Y : Type} (x : I → X) (y : I → Y)
    (accepts : X → Y → Prop) (left : G → X → Prop) (right : G → Y → Prop)
    (inside : ∀ g a b, left g a → right g b → accepts a b)
    (choose : I → G) (covers : ∀ i, left (choose i) (x i) ∧ right (choose i) (y i))
    (independent : ∀ i j, i ≠ j → ¬ accepts (x i) (y j)) :
    ∀ i j, choose i = choose j → i = j := by
  intro i j same
  by_cases e : i = j
  · exact e
  · have r := (covers j).2
    rw [← same] at r
    exact False.elim (independent i j e (inside _ _ _ (covers i).1 r))
#print axioms selected_injection
end RectangleCover
