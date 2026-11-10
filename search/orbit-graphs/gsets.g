# gsets.g -- export all transitive actions G/H (H up to conjugacy, [G:H] <= MAXIDX)
# of a group G, as permutations of a common generating set, for orbsearch.
#
# Usage (from a driver): define GRP (a group), GNAME (string), MAXIDX (int),
# MINSTABIDX (optional) and OUTFILE, then Read("gsets.g");
#
# Output format (0-based permutations):
#   GROUP <name> <order> <ngens>
#   ACTION <k> <index> <stabilizer order> <stabilizer description>
#   <images of generator 1 on 0..index-1>
#   ...
#   END

ExportGSets := function(G, gname, maxidx, outfile)
  local gens, P, iso, subs, out, k, H, idx, hom, imgs, g, desc, ord, t0;
  t0 := Runtime();
  if not IsPermGroup(G) then
    iso := IsomorphismPermGroup(G);
    P := Image(iso);
    P := Group(SmallGeneratingSet(P));
  else
    P := Group(SmallGeneratingSet(G));
  fi;
  gens := GeneratorsOfGroup(P);
  ord := Size(P);
  subs := LowIndexSubgroups(P, maxidx);
  out := OutputTextFile(outfile, false);
  SetPrintFormattingStatus(out, false);
  AppendTo(out, "GROUP ", gname, " ", ord, " ", Length(gens), "\n");
  k := 0;
  for H in subs do
    idx := Index(P, H);
    if idx > 1 then
      hom := FactorCosetAction(P, H);
      imgs := List(gens, g -> ListPerm(Image(hom, g), idx) - 1);
      desc := "-";
      AppendTo(out, "ACTION ", k, " ", idx, " ", Size(H), " ", desc, "\n");
      for g in imgs do
        AppendTo(out, JoinStringsWithSeparator(List(g, String), " "), "\n");
      od;
      k := k + 1;
    fi;
  od;
  AppendTo(out, "END\n");
  CloseStream(out);
  return [k, Runtime() - t0];
end;
