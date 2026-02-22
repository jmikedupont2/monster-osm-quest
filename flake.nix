{
  description = "Monster OSM Quest - Standalone browser game";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        packages.default = pkgs.stdenv.mkDerivation {
          name = "monster-osm-quest";
          src = ./.;
          
          installPhase = ''
            mkdir -p $out
            cp index.html $out/
            cp game.js $out/
            cp README.md $out/
          '';
        };

        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            python3
            nodejs
          ];
          
          shellHook = ''
            echo "🎭 Monster OSM Quest - Dev Environment"
            echo ""
            echo "Commands:"
            echo "  python3 -m http.server 8888  # Start local server"
            echo "  Open http://localhost:8888"
            echo ""
          '';
        };

        apps.default = {
          type = "app";
          program = "${pkgs.writeShellScript "serve-monster-quest" ''
            cd ${self.packages.${system}.default}
            ${pkgs.python3}/bin/python3 -m http.server 8888
          ''}";
        };
      }
    );
}
